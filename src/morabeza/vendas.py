"""Vendas da Morabeza em Python idiomático (Sessão 2).

Cada venda passa a ser um objeto Venda (dataclass) em vez de um dicionário.
Linhas com erros levantam VendaInvalida e são postas de parte na leitura.
"""
from __future__ import annotations

import csv
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date

ILHAS_SERVIDAS = {"Santiago", "São Vicente", "Sal", "Boa Vista", "Fogo", "Santo Antão"}


class VendaInvalida(Exception):
    """Uma linha do ficheiro de vendas não pode ser transformada numa Venda."""


@dataclass(frozen=True)
class Venda:
    venda_id: str
    data: date
    cliente_id: str
    ilha: str
    categoria: str
    quantidade: int
    preco_unitario: int

    @property
    def total(self) -> int:
        """Valor da venda em escudos."""
        # TODO 1: devolve a quantidade vezes o preço unitário (usa self.).
        return self.quantidade * self.preco_unitario


def criar_venda(linha: dict[str, str]) -> Venda:
    """Converte uma linha do CSV numa Venda, ou levanta VendaInvalida."""
    # TODO 2: dentro de um try, converte quantidade e preco_unitario com int()
    #         e a data com date.fromisoformat(). Se der ValueError, levanta
    #         VendaInvalida (raise VendaInvalida("...") from erro).
    # TODO 3: levanta VendaInvalida se a quantidade ou o preço não forem > 0,
    #         ou se linha["ilha"] não estiver em ILHAS_SERVIDAS.
    # TODO 4: devolve Venda(...) com os valores já convertidos.
    try:
        quantidade = int(linha["quantidade"])
        preco_unitario = int(linha["preco_unitario"])
        data_venda = date.fromisoformat(linha["data"])
    except ValueError as erro:
        raise VendaInvalida("Quantidade, preço ou data inválidos.") from erro

    if quantidade <= 0:
        raise VendaInvalida("A quantidade deve ser maior que zero.")

    if preco_unitario <= 0:
        raise VendaInvalida("O preço unitário deve ser maior que zero.")

    if linha["ilha"] not in ILHAS_SERVIDAS:
        raise VendaInvalida("Ilha não servida.")

    return Venda(
        venda_id=linha["venda_id"],
        data=data_venda,
        cliente_id=linha["cliente_id"],
        ilha=linha["ilha"],
        categoria=linha["categoria"],
        quantidade=quantidade,
        preco_unitario=preco_unitario
    )


def ler_vendas(caminho: str) -> Iterator[Venda]:
    """Gerador: devolve, uma a uma, as vendas válidas do ficheiro. As inválidas são ignoradas."""
    # TODO 5: abre o ficheiro e percorre csv.DictReader. Para cada linha,
    #         tenta yield criar_venda(linha); se der VendaInvalida, continue.
    #         Repara: é um gerador, por isso usa yield e não return.
    with open(caminho, mode="r", encoding="utf-8", newline="") as ficheiro:
        leitor = csv.DictReader(ficheiro)

        for linha in leitor:
            try:
                yield criar_venda(linha)
            except VendaInvalida:
                continue


def contar_invalidas(caminho: str) -> int:
    """Número de linhas do ficheiro que não dão uma Venda válida."""
    # TODO 6: igual a ler_vendas, mas em vez de devolver vendas conta quantas
    #         linhas levantam VendaInvalida e devolve esse número.
    invalidas = 0

    with open(caminho, mode="r", encoding="utf-8", newline="") as ficheiro:
        leitor = csv.DictReader(ficheiro)

        for linha in leitor:
            try:
                criar_venda(linha)
            except VendaInvalida:
                invalidas += 1

    return invalidas


def vendas_acima(vendas: Iterable[Venda], limite: int) -> list[Venda]:
    """Vendas com total maior do que o limite, numa compreensão de lista."""
    # TODO 7: uma só linha com uma compreensão de lista: [v for v in ... if ...]
    return [v for v in vendas if v.total > limite]


def total_por(vendas: Iterable[Venda], chave: Callable[[Venda], str]) -> dict[str, int]:
    """Soma dos totais agrupada pela função chave. Ex.: total_por(vendas, lambda v: v.ilha)."""
    # TODO 8: igual a faturacao_por_ilha da Sessão 1, mas a chave do dicionário
    #         é chave(v) em vez de v["ilha"]. Assim a mesma função serve para
    #         agrupar por ilha, por categoria ou por mês.
    totais: dict[str, int] = {}

    for v in vendas:
        grupo = chave(v)
        totais[grupo] = totais.get(grupo, 0) + v.total

    return totais

# ---------------------------------------------------------------- Extensão (opcional)

def top_n(totais: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Os n pares (chave, total) com maior total, do maior para o menor."""
    # EXTENSÃO: sorted(totais.items(), key=lambda par: ..., reverse=True) e depois [:n]
    return sorted(totais.items(), key=lambda par: par[1], reverse=True)[:n]


@contextmanager
def cronometro(nome: str):
    """Mede o tempo de um bloco. Uso: with cronometro("leitura"): ..."""
    # EXTENSÃO: guarda time.perf_counter() antes do yield e, num finally,
    #           imprime f"{nome}: {segundos:.3f} s".
    inicio = time.perf_counter()

    try:
        yield
    finally:
        segundos = time.perf_counter() - inicio
        print(f"{nome}: {segundos:.3f} s")
