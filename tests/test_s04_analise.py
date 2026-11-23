"""Testes do Laboratório 4 (Sessão 7). Corre: pytest tests/test_s04_analise.py -v"""
from pathlib import Path

import pandas as pd
import pytest

from morabeza import analise

PASTA = Path(__file__).parent.parent / "data" / "tabelas"


@pytest.fixture(scope="module")
def df():
    vendas, clientes, produtos = analise.carregar(str(PASTA))
    return analise.juntar(vendas, clientes, produtos)


def test_carregar_le_as_tres_tabelas_com_datas():
    vendas, clientes, produtos = analise.carregar(str(PASTA))
    assert (len(vendas), len(clientes), len(produtos)) == (33788, 480, 32)
    assert pd.api.types.is_datetime64_any_dtype(vendas["data"]), "usa parse_dates=['data']"


def test_juntar(df):
    assert len(df) == 33788, "o merge não pode criar nem perder linhas"
    assert {"tipo", "ilha", "nome", "categoria", "total"} <= set(df.columns)
    assert df["total"].sum() == 171752890


def test_faturacao_mensal_por_ilha(df):
    tabela = analise.faturacao_mensal_por_ilha(df)
    assert tabela.shape == (24, 6)
    assert tabela.loc["2025-03", "Sal"] == 1256860


def test_top_produtos(df):
    top = analise.top_produtos(df, 3)
    assert list(top.index) == ["Detergente roupa 3 kg", "Grogue 70 cl", "Papel higiénico (12 rolos)"]
    assert top.iloc[0] == 23057500


def test_quota_por_tipo(df):
    quota = analise.quota_por_tipo(df)
    assert quota["HORECA"] == 57.8
    assert abs(quota.sum() - 100) < 0.2


def test_aplicar_desconto(df):
    com = analise.aplicar_desconto(df)
    assert "total_com_desconto" not in df.columns, "não alteres o df original: usa df.copy()"
    assert round(com["total_com_desconto"].sum(), 1) == 166283437.5


# ---------------------------------------------------------------- Extensão (aparece SKIPPED se por fazer)

def _ou_saltar(f, *a):
    try:
        return f(*a)
    except NotImplementedError:
        pytest.skip("extensão por fazer")


def test_extensao_otimizar_tipos(df):
    otimizado = _ou_saltar(analise.otimizar_tipos, df)
    assert otimizado.memory_usage(deep=True).sum() < df.memory_usage(deep=True).sum() / 2
    assert otimizado["total"].sum() == df["total"].sum()


def test_extensao_formato_longo(df):
    longo = _ou_saltar(analise.formato_longo, analise.faturacao_mensal_por_ilha(df))
    assert list(longo.columns) == ["mes", "ilha", "total"]
    assert len(longo) == 144
