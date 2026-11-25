"""Lab 5 · Extrair de quatro fontes.

As fontes estão em data/fontes_s1_2025/. Testa com:
    pytest tests/test_etl_lab5.py -v
"""

import json  # noqa: F401  (vais precisar)
import sqlite3  # noqa: F401

import pandas as pd  # noqa: F401


def ler_vendas_csv(caminho):
    """Lê o CSV de vendas com TUDO como texto (dtype=str), para não perder
    informação antes de limpar."""
    df = pd.read_csv(caminho, dtype=str)
    return df


def ler_produtos_excel(caminho):
    """Lê a folha 'produtos' do Excel."""
    df = pd.read_excel(caminho, sheet_name="produtos")
    return df


def ler_clientes_sqlite(caminho):
    """SELECT * FROM clientes. Dica: pd.read_sql_query(sql, conn)"""
    conn = sqlite3.connect(caminho)
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    return df


def ler_promocoes_json(caminho):
    """O ficheiro imita a resposta de uma API: os registos estão em 'dados'.
    Se 'estado' não for 'ok', levanta ValueError."""
    with open(caminho, "r", encoding="utf-8") as ficheiro:
        dados = json.load(ficheiro)

    if dados["estado"] != "ok":
        raise ValueError("Estado da API não é ok")

    return pd.DataFrame(dados["dados"])
