"""Peças já prontas para o pipeline do Laboratório 6 (vêm da solução do Laboratório 5). Não precisas de as alterar."""
import sqlite3

import pandas as pd


def limpar(vendas: pd.DataFrame) -> pd.DataFrame:
    """Limpeza do Laboratório 5, resumida: duplicados, datas, números e linhas inválidas."""
    df = vendas.drop_duplicates().copy()
    iso = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["data"] = iso.fillna(pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")).dt.strftime("%Y-%m-%d")
    for coluna in ["quantidade", "preco_unitario"]:
        df[coluna] = df[coluna].str.extract(r"(-?\d+)")[0].astype("Int64")
    validas = df["cliente_id"].notna() & df["data"].notna() & (df["quantidade"] > 0) & (df["preco_unitario"] > 0)
    return df[validas.fillna(False)].reset_index(drop=True)


def criar_tabelas(conn: sqlite3.Connection) -> None:
    """Cria as tabelas de destino, se ainda não existirem."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vendas (
            venda_id TEXT PRIMARY KEY, data TEXT, cliente_id TEXT, produto_id TEXT,
            quantidade INTEGER, preco_unitario INTEGER);
        CREATE TABLE IF NOT EXISTS ficheiros_processados (
            nome TEXT PRIMARY KEY, linhas INTEGER, processado_em TEXT);
    """)


def contar(conn: sqlite3.Connection, tabela: str) -> int:
    """Número de linhas de uma tabela."""
    return conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
