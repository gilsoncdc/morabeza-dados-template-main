"""Testes do Laboratório 6 (Sessão 9). Corre: pytest tests/test_s06_pipeline.py -v"""
import shutil
import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from morabeza.etl import pipeline
from morabeza.etl.base_pipeline import contar, criar_tabelas

BRUTOS = Path(__file__).parent.parent / "data" / "brutos"


@pytest.fixture
def ambiente(tmp_path):
    pasta = tmp_path / "mensais"
    shutil.copytree(BRUTOS / "mensais", pasta)
    return str(pasta), str(tmp_path / "morabeza.db")


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    criar_tabelas(c)
    yield c
    c.close()


def test_ficheiros_pendentes(ambiente, conn):
    pasta, _ = ambiente
    assert [p.name for p in pipeline.ficheiros_pendentes(pasta, conn)][:2] == ["vendas_2025-01.csv", "vendas_2025-02.csv"]
    conn.execute("INSERT INTO ficheiros_processados VALUES ('vendas_2025-01.csv', 1, 'x')")
    assert len(pipeline.ficheiros_pendentes(pasta, conn)) == 5


def test_carregar_vendas_e_idempotente(conn):
    df = pd.DataFrame({"venda_id": ["V1", "V2"], "data": ["2025-01-01"] * 2, "cliente_id": ["C1"] * 2,
                       "produto_id": ["P1"] * 2, "quantidade": [1, 2], "preco_unitario": [100, 200]})
    assert pipeline.carregar_vendas(df, conn) == 2
    pipeline.carregar_vendas(df, conn)
    assert contar(conn, "vendas") == 2, "correr duas vezes não pode duplicar"


def test_processar_ficheiro_regista_o_ficheiro(ambiente, conn):
    pasta, _ = ambiente
    n = pipeline.processar_ficheiro(Path(pasta) / "vendas_2025-01.csv", conn)
    assert n == contar(conn, "vendas") == 1665
    assert contar(conn, "ficheiros_processados") == 1


def test_correr_isola_o_ficheiro_corrompido(ambiente):
    r = pipeline.correr(*ambiente)
    assert r["falhados"] == ["vendas_2025-04.csv"]
    assert len(r["processados"]) == 5
    assert r["linhas"] == 7708


def test_correr_duas_vezes_nao_muda_nada(ambiente):
    pipeline.correr(*ambiente)
    r = pipeline.correr(*ambiente)
    assert r["processados"] == [] and r["linhas"] == 7708


def test_correr_e_incremental(ambiente):
    pasta, bd = ambiente
    pipeline.correr(pasta, bd)
    shutil.copy(BRUTOS / "novos" / "vendas_2025-07.csv", pasta)
    r = pipeline.correr(pasta, bd)
    assert r["processados"] == ["vendas_2025-07.csv"]
    assert r["linhas"] == 9117


# ---------------------------------------------------------------- Extensão (aparece SKIPPED se por fazer)

def test_extensao_reprocessar_nao_duplica(ambiente):
    pasta, bd = ambiente
    pipeline.correr(pasta, bd)
    with sqlite3.connect(bd) as c:
        try:
            pipeline.esquecer_ficheiro("vendas_2025-01.csv", c)
        except NotImplementedError:
            pytest.skip("extensão por fazer")
    r = pipeline.correr(pasta, bd)
    assert r["processados"] == ["vendas_2025-01.csv"] and r["linhas"] == 7708
