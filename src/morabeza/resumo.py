"""Resumo das vendas da Morabeza Distribuição (Sessão 1).

Lê um ficheiro CSV de vendas e mostra a faturação total e por ilha.
Só usa a biblioteca padrão do Python: o pandas chega na Sessão 4.
"""
import csv
import sys


def ler_vendas(caminho: str) -> list[dict]:
    """Lê o CSV de vendas e devolve uma lista de dicionários, um por venda.

    O módulo csv lê tudo como texto. As colunas quantidade e preco_unitario
    têm de ser convertidas para int, senão as contas dão resultados errados.
    """
    # TODO 1: abre o ficheiro com open(caminho, encoding="utf-8") dentro de um with.
    # TODO 2: percorre as linhas com csv.DictReader(ficheiro).
    # TODO 3: converte linha["quantidade"] e linha["preco_unitario"] para int.
    # TODO 4: junta cada linha a uma lista e devolve a lista no fim.
    raise NotImplementedError("ler_vendas ainda não está feita")


def total_venda(venda: dict) -> int:
    """Valor de uma venda em escudos: quantidade vezes preço unitário."""
    # TODO: devolve a quantidade vezes o preço unitário.
    raise NotImplementedError("total_venda ainda não está feita")


def faturacao_total(vendas: list[dict]) -> int:
    """Soma do valor de todas as vendas."""
    # TODO: começa com total = 0 e soma total_venda(venda) de cada venda.
    raise NotImplementedError("faturacao_total ainda não está feita")


def faturacao_por_ilha(vendas: list[dict]) -> dict[str, int]:
    """Dicionário {ilha: faturação} com a soma das vendas de cada ilha."""
    # TODO: cria um dicionário vazio e, para cada venda, soma total_venda(venda)
    # na chave da ilha respetiva. Dica: por_ilha.get(ilha, 0) devolve 0 se a ilha ainda não existir.
    raise NotImplementedError("faturacao_por_ilha ainda não está feita")


def ilha_top(por_ilha: dict[str, int]) -> str:
    """Nome da ilha com maior faturação."""
    # TODO: devolve a chave com o maior valor. Dica: max(por_ilha, key=por_ilha.get).
    raise NotImplementedError("ilha_top ainda não está feita")


# ---------------------------------------------------------------- Extensão (opcional)

def faturacao_mensal(vendas: list[dict]) -> dict[str, int]:
    """Dicionário {"AAAA-MM": faturação}, ordenado por mês."""
    # EXTENSÃO: igual a faturacao_por_ilha, mas a chave é o mês. O mês são os
    # 7 primeiros caracteres da data: venda["data"][:7] dá "2025-01".
    # No fim devolve o dicionário ordenado: dict(sorted(por_mes.items())).
    raise NotImplementedError("Extensão por fazer")


def formatar_cve(valor: int) -> str:
    """Formata um valor em escudos com espaço a separar os milhares: 1530740 -> '1 530 740 CVE'."""
    # EXTENSÃO: f"{valor:,}" dá "1,530,740". Troca as vírgulas por espaços e junta " CVE".
    raise NotImplementedError("Extensão por fazer")


# ---------------------------------------------------------------- Programa principal

def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Uso: python -m morabeza.resumo <ficheiro.csv>")
        sys.exit(1)

    caminho = argv[1]
    vendas = ler_vendas(caminho)
    por_ilha = faturacao_por_ilha(vendas)

    print(f"Resumo de vendas: {caminho}")
    print(f"Número de vendas: {len(vendas)}")
    print(f"Faturação total: {faturacao_total(vendas)} CVE")
    print("Faturação por ilha:")
    for ilha, valor in sorted(por_ilha.items(), key=lambda par: par[1], reverse=True):
        print(f"  {ilha}: {valor} CVE")
    print(f"Ilha com maior faturação: {ilha_top(por_ilha)}")


if __name__ == "__main__":
    main(sys.argv)
