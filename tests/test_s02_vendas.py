"""Testes do laboratório da Sessão 2. Corre: pytest tests/test_s02_vendas.py -v"""
from datetime import date
from pathlib import Path

import pytest

from morabeza.vendas import (
    Venda,
    VendaInvalida,
    contar_invalidas,
    criar_venda,
    ler_vendas,
    total_por,
    vendas_acima,
)

DADOS = Path(__file__).parent.parent / "data" / "vendas_s02.csv"
LINHA = {"venda_id": "V1", "data": "2025-01-05", "cliente_id": "C1", "ilha": "Sal",
         "categoria": "Bebidas", "quantidade": "2", "preco_unitario": "100"}


def test_total_da_venda():
    v = Venda("V1", date(2025, 1, 5), "C1", "Sal", "Bebidas", 3, 50)
    assert v.total == 150


def test_criar_venda_converte_tipos():
    v = criar_venda(LINHA)
    assert v == Venda("V1", date(2025, 1, 5), "C1", "Sal", "Bebidas", 2, 100)


@pytest.mark.parametrize("campo, valor", [
    ("quantidade", "0"), ("quantidade", "-3"), ("quantidade", "dez"), ("preco_unitario", ""),
    ("preco_unitario", "-150"), ("ilha", "Brava"), ("data", "2025-02-29"), ("data", "09/03/2025"),
])
def test_criar_venda_rejeita_linhas_invalidas(campo, valor):
    with pytest.raises(VendaInvalida):
        criar_venda({**LINHA, campo: valor})


def test_ler_vendas_e_um_gerador_que_ignora_invalidas():
    vendas = ler_vendas(str(DADOS))
    assert not isinstance(vendas, list), "ler_vendas deve usar yield (gerador)"
    vendas = list(vendas)
    assert len(vendas) == 300
    assert sum(v.total for v in vendas) == 1530740


def test_contar_invalidas():
    assert contar_invalidas(str(DADOS)) == 12


def test_vendas_acima():
    vendas = list(ler_vendas(str(DADOS)))
    assert len(vendas_acima(vendas, 20000)) == 9


def test_total_por_ilha_e_por_categoria():
    vendas = list(ler_vendas(str(DADOS)))
    assert total_por(vendas, lambda v: v.ilha)["Sal"] == 226410
    assert total_por(vendas, lambda v: v.categoria)["Limpeza"] == 448670


# ---------------------------------------------------------------- Extensão (aparece SKIPPED se por fazer)

def _ou_saltar(f, *a):
    try:
        return f(*a)
    except NotImplementedError:
        pytest.skip("extensão por fazer")


def test_extensao_top_n():
    from morabeza.vendas import top_n
    assert _ou_saltar(top_n, {"a": 1, "b": 5, "c": 3}, 2) == [("b", 5), ("c", 3)]


def test_extensao_cronometro(capsys):
    from morabeza.vendas import cronometro
    try:
        with cronometro("teste"):
            sum(range(1000))
    except NotImplementedError:
        pytest.skip("extensão por fazer")
    assert capsys.readouterr().out.startswith("teste: ")
