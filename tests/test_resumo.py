"""Testes do laboratório da Sessão 1.

Não precisas de alterar este ficheiro. Corre `pytest -v` e vai fazendo as
funções em src/morabeza/resumo.py até todos os testes ficarem a verde (PASSED).
"""
from pathlib import Path

import pytest

from morabeza import resumo

CSV_PEQUENO = """venda_id,data,cliente_id,ilha,categoria,quantidade,preco_unitario
V1,2025-01-05,C1,Sal,Bebidas,2,100
V2,2025-01-20,C2,Santiago,Mercearia,3,50
V3,2025-02-02,C1,Sal,Limpeza,1,1000
"""

AMOSTRA = Path(__file__).parent.parent / "data" / "vendas_amostra.csv"


@pytest.fixture
def vendas_pequenas(tmp_path):
    caminho = tmp_path / "vendas.csv"
    caminho.write_text(CSV_PEQUENO, encoding="utf-8")
    return resumo.ler_vendas(str(caminho))


def test_ler_vendas_le_todas_as_linhas(vendas_pequenas):
    assert len(vendas_pequenas) == 3


def test_ler_vendas_converte_numeros_para_int(vendas_pequenas):
    primeira = vendas_pequenas[0]
    assert primeira["quantidade"] == 2, "a quantidade deve ser o número 2 e não o texto '2'"
    assert primeira["preco_unitario"] == 100


def test_total_venda():
    assert resumo.total_venda({"quantidade": 3, "preco_unitario": 50}) == 150


def test_faturacao_total(vendas_pequenas):
    assert resumo.faturacao_total(vendas_pequenas) == 1350


def test_faturacao_por_ilha(vendas_pequenas):
    assert resumo.faturacao_por_ilha(vendas_pequenas) == {"Sal": 1200, "Santiago": 150}


def test_ilha_top():
    assert resumo.ilha_top({"Sal": 1200, "Santiago": 150, "Fogo": 900}) == "Sal"


def test_amostra_real():
    vendas = resumo.ler_vendas(str(AMOSTRA))
    assert len(vendas) == 300
    assert resumo.faturacao_total(vendas) == 1530740
    assert resumo.ilha_top(resumo.faturacao_por_ilha(vendas)) == "Santiago"


# ---------------------------------------------------------------- Extensão (opcional)
# Estes testes aparecem como SKIPPED enquanto a extensão não estiver feita.

def _ou_saltar(funcao, *args):
    try:
        return funcao(*args)
    except NotImplementedError:
        pytest.skip("extensão por fazer")


def test_extensao_faturacao_mensal(vendas_pequenas):
    resultado = _ou_saltar(resumo.faturacao_mensal, vendas_pequenas)
    assert resultado == {"2025-01": 350, "2025-02": 1000}
    assert list(resultado) == ["2025-01", "2025-02"]


def test_extensao_formatar_cve():
    assert _ou_saltar(resumo.formatar_cve, 1530740) == "1 530 740 CVE"
    assert _ou_saltar(resumo.formatar_cve, 950) == "950 CVE"
