"""Testes do Lab 5 (extrair e transformar). Correr: pytest tests/test_etl_lab5.py -v"""

from pathlib import Path

import pandas as pd
import pytest

from morabeza.etl import extrair, transformar

FONTES = Path(__file__).resolve().parents[1] / "data" / "fontes_s1_2025"


# ------------------------------------------------------------------ extrair
def test_ler_vendas_csv_tudo_texto():
    df = extrair.ler_vendas_csv(FONTES / "vendas_s1_2025.csv")
    assert len(df) == 9896
    assert df["quantidade"].dropna().map(type).eq(str).all(), "use dtype=str"


def test_ler_outras_fontes():
    assert len(extrair.ler_produtos_excel(FONTES / "produtos.xlsx")) == 40
    assert len(extrair.ler_clientes_sqlite(FONTES / "clientes.sqlite")) == 477
    promos = extrair.ler_promocoes_json(FONTES / "promocoes.json")
    assert len(promos) == 4
    assert "desconto_pct" in promos.columns


def test_promocoes_estado_erro(tmp_path):
    f = tmp_path / "erro.json"
    f.write_text('{"estado": "erro", "dados": []}', encoding="utf-8")
    with pytest.raises(ValueError):
        extrair.ler_promocoes_json(f)


# --------------------------------------------------------------- transformar
@pytest.mark.parametrize("bruto, esperado", [
    ("Santiago", "Santiago"), ("SANTIAGO", "Santiago"), ("santiago ", "Santiago"),
    ("Sao Vicente", "São Vicente"), ("S. Vicente", "São Vicente"),
    ("Boavista", "Boa Vista"), (" sal", "Sal"), ("Santo Antao", "Santo Antão"),
    ("Maio", None), ("", None), (None, None),
])
def test_normalizar_ilha(bruto, esperado):
    assert transformar.normalizar_ilha(bruto) == esperado


def test_normalizar_data_dois_formatos():
    assert transformar.normalizar_data("2025-03-01") == pd.Timestamp("2025-03-01")
    assert transformar.normalizar_data("01/03/2025") == pd.Timestamp("2025-03-01")
    assert pd.isna(transformar.normalizar_data("29/02/2025"))


def test_limpar_numero():
    s = pd.Series(["12", "12 un", "3 unidades", "1250 CVE", None])
    r = transformar.limpar_numero(s)
    assert r.iloc[:4].tolist() == [12.0, 12.0, 3.0, 1250.0]
    assert pd.isna(r.iloc[4])


def test_remover_duplicados():
    df = pd.DataFrame({"venda_id": ["V1", "V2", "V1"], "x": [1, 2, 1]})
    assert transformar.remover_duplicados(df)["venda_id"].tolist() == ["V1", "V2"]


def test_limpar_vendas_resultado():
    bruto = extrair.ler_vendas_csv(FONTES / "vendas_s1_2025.csv")
    limpo = transformar.limpar_vendas(bruto)
    assert len(limpo) == 9568
    assert limpo["venda_id"].is_unique
    assert set(limpo["ilha"]) <= set(transformar.ILHAS_VALIDAS)
    assert (limpo["quantidade"] * limpo["preco_unitario"]).sum() == 52_773_085


def test_limpar_vendas_e_pura():
    bruto = extrair.ler_vendas_csv(FONTES / "vendas_s1_2025.csv")
    copia = bruto.copy()
    transformar.limpar_vendas(bruto)
    pd.testing.assert_frame_equal(bruto, copia)
