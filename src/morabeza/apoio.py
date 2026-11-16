"""Funções de apoio já prontas (vêm da solução da Sessão 1). Não precisas de as alterar."""
import csv


def ler_vendas(caminho: str) -> list[dict]:
    vendas = []
    with open(caminho, encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            linha["quantidade"] = int(linha["quantidade"])
            linha["preco_unitario"] = int(linha["preco_unitario"])
            vendas.append(linha)
    return vendas


def total_venda(venda: dict) -> int:
    return venda["quantidade"] * venda["preco_unitario"]


def faturacao_por_ilha(vendas: list[dict]) -> dict[str, int]:
    por_ilha: dict[str, int] = {}
    for venda in vendas:
        por_ilha[venda["ilha"]] = por_ilha.get(venda["ilha"], 0) + total_venda(venda)
    return por_ilha
