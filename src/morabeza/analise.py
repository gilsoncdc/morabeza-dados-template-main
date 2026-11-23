"""Laboratório 4 (Sessão 7): painel de vendas da Morabeza com pandas e NumPy.

Trabalha com as tabelas completas de 2024 e 2025: vendas, clientes e produtos.
"""
from pathlib import Path

import numpy as np
import pandas as pd


def carregar(pasta: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Lê vendas.csv, clientes.csv e produtos.csv da pasta, com os tipos certos."""
    pasta = Path(pasta)  # já feito: assim podes escrever pasta / "vendas.csv"
    # TODO 1: lê os três ficheiros com pd.read_csv(pasta / "nome.csv").
    #         Nas vendas usa parse_dates=["data"]; nos clientes, parse_dates=["data_registo"].
    #         Devolve (vendas, clientes, produtos), por esta ordem.
    vendas = pd.read_csv(pasta / "vendas.csv", parse_dates=["data"])
    clientes = pd.read_csv(pasta / "clientes.csv", parse_dates=["data_registo"])
    produtos = pd.read_csv(pasta / "produtos.csv")

    return vendas, clientes, produtos


def juntar(vendas: pd.DataFrame, clientes: pd.DataFrame, produtos: pd.DataFrame) -> pd.DataFrame:
    """Uma tabela única: cada venda com a ilha e o tipo do cliente, o produto e o total."""
    # TODO 2: junta às vendas as colunas cliente_id, tipo e ilha dos clientes (merge on="cliente_id")
    #         e as colunas produto_id, nome e categoria dos produtos (merge on="produto_id").
    # TODO 3: cria a coluna total = quantidade * preco_unitario (numa linha, sem ciclos).
    df = vendas.merge(clientes[["cliente_id", "tipo", "ilha"]],
        on="cliente_id",
        how="left").merge(produtos[["produto_id", "nome", "categoria"]],
        on="produto_id", how="left")

    df["total"] = df["quantidade"] * df["preco_unitario"]

    return df


def faturacao_mensal_por_ilha(df: pd.DataFrame) -> pd.DataFrame:
    """Tabela com uma linha por mês ("AAAA-MM"), uma coluna por ilha e a faturação nas células."""
    # TODO 4: cria uma coluna mes com df["data"].dt.strftime("%Y-%m") e usa
    #         pivot_table(index="mes", columns="ilha", values="total", aggfunc="sum", fill_value=0).
    df = df.assign(mes=df["data"].dt.strftime("%Y-%m"))

    return df.pivot_table(
        index="mes",
        columns="ilha",
        values="total",
        aggfunc="sum",
        fill_value=0
    )


def top_produtos(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Os n produtos com maior faturação, do maior para o menor."""
    # TODO 5: groupby("nome")["total"].sum(), ordena do maior para o menor e fica com os n primeiros.
    return df.groupby("nome")["total"].sum().sort_values(ascending=False).head(n)


def quota_por_tipo(df: pd.DataFrame) -> pd.Series:
    """Percentagem da faturação por tipo de cliente, arredondada a uma casa decimal."""
    # TODO 6: soma o total por tipo, divide pela soma de tudo, multiplica por 100 e arredonda (round(1)).
    
    faturacao_tipo = df.groupby("tipo")["total"].sum()
    quota = (faturacao_tipo / df["total"].sum()) * 100

    return quota.round(1)


def aplicar_desconto(df: pd.DataFrame) -> pd.DataFrame:
    """Acrescenta total_com_desconto: 5% de desconto nas linhas com 20 ou mais unidades.

    Vetorizado com np.where, sem ciclos for.
    """
    df = df.copy()
    # TODO 7: df["total_com_desconto"] = np.where(condição, valor_se_verdade, valor_se_falso)
    #         Condição: quantidade >= 20. Com desconto: total * 0.95. Sem desconto: total.

    df["total_com_desconto"] = np.where(
        df["quantidade"] >= 20,
        df["total"] * 0.95,
        df["total"]
    )

    return df


# ---------------------------------------------------------------- Extensão (opcional)

def otimizar_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas de texto repetitivo em category e reduz os inteiros."""
    # EXTENSÃO: astype("category") nas colunas de texto que se repetem (ilha, tipo, categoria,
    #           nome, produto_id) e pd.to_numeric(..., downcast="integer") em quantidade e preco_unitario.
    df = df.copy()

    colunas = ["ilha", "tipo", "categoria", "nome", "produto_id"]

    for coluna in colunas:
        df[coluna] = df[coluna].astype("category")

    df["quantidade"] = pd.to_numeric(
        df["quantidade"], downcast="integer"
    )

    df["preco_unitario"] = pd.to_numeric(
        df["preco_unitario"], downcast="integer"
    )

    return df


def formato_longo(tabela: pd.DataFrame) -> pd.DataFrame:
    """Passa a tabela mensal (uma coluna por ilha) para formato longo: mes, ilha, total."""
    # EXTENSÃO: tabela.reset_index().melt(id_vars="mes", var_name="ilha", value_name="total")
    return tabela.reset_index().melt(
        id_vars="mes",
        var_name="ilha",
        value_name="total"
    )
