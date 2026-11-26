"""Laboratório 6 (Sessão 9): pipeline incremental e idempotente das vendas mensais.

Uso:  python -m morabeza.etl.pipeline data/brutos/mensais morabeza.db
"""
import argparse
import logging
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from morabeza.etl.base_pipeline import contar, criar_tabelas, limpar

logger = logging.getLogger(__name__)
COLUNAS = ["venda_id", "data", "cliente_id", "produto_id", "quantidade", "preco_unitario"]


def ficheiros_pendentes(pasta: str, conn: sqlite3.Connection) -> list[Path]:
    """Ficheiros vendas_*.csv da pasta que ainda não estão em ficheiros_processados, por ordem de nome."""
    # TODO 1: lê os nomes já processados: conn.execute("SELECT nome FROM ficheiros_processados")
    #         devolve tuplos; guarda o primeiro elemento de cada um num conjunto.
    # TODO 2: devolve, ordenados, os Path(pasta).glob("vendas_*.csv") cujo .name não está no conjunto.
    # TODO 1: Ler os nomes dos ficheiros já processados
    registos = conn.execute("SELECT nome FROM ficheiros_processados").fetchall()
    processados = {registo[0] for registo in registos}
    pendentes = [ 
        ficheiro
        for ficheiro in Path(pasta).glob("vendas_*.csv")
        if ficheiro.name not in processados
    ]
    return sorted(pendentes)


def carregar_vendas(df: pd.DataFrame, conn: sqlite3.Connection) -> int:
    """Grava as vendas com INSERT OR REPLACE: correr duas vezes não duplica linhas. Devolve o número de linhas."""
    # JÁ FEITA: lê-a e percebe-a, não precisas de a alterar.
    # 1. Cada venda passa a ser um tuplo com as 6 colunas, pela ordem da tabela.
    linhas = list(df[COLUNAS].astype(object).itertuples(index=False, name=None))
    # 2. Um único executemany grava todas as linhas. Cada ? recebe um valor, separado do SQL.
    #    O OR REPLACE torna a carga idempotente: um venda_id que já existe é substituído, não duplicado.
    conn.executemany("INSERT OR REPLACE INTO vendas VALUES (?, ?, ?, ?, ?, ?)", linhas)
    return len(linhas)


def processar_ficheiro(caminho: Path, conn: sqlite3.Connection) -> int:
    """Lê, limpa e carrega um ficheiro, e regista-o como processado, tudo numa só transação."""
    df = limpar(pd.read_csv(caminho, dtype=str))
    # TODO 3: dentro de um bloco with conn: (uma transação), chama carregar_vendas e regista o ficheiro
    #         com INSERT INTO ficheiros_processados VALUES (?, ?, ?): nome, número de linhas e
    #         datetime.now(timezone.utc).isoformat(timespec="seconds"). Devolve o número de linhas.
    with conn:
        numero_linhas = carregar_vendas(df, conn)
        conn.execute("INSERT INTO ficheiros_processados VALUES (?, ?, ?)",
            (caminho.name, numero_linhas, datetime.now(timezone.utc).isoformat(timespec="seconds"))
        )

    return numero_linhas


def correr(pasta: str, caminho_bd: str) -> dict:
    """Processa os ficheiros pendentes. Um ficheiro com erro é registado e não trava os outros."""
    relatorio = {"processados": [], "falhados": [], "linhas": 0}
    with sqlite3.connect(caminho_bd) as conn:
        criar_tabelas(conn)
        # TODO 4: para cada ficheiro pendente, tenta processar_ficheiro.
        #         Se der KeyError ou ValueError: logger.error(...), junta o nome a "falhados" e continua.
        #         Se correr bem: logger.info("Carreguei %d vendas de %s", ...) e junta a "processados".
        # TODO 5: no fim, relatorio["linhas"] = contar(conn, "vendas").
        for ficheiro in ficheiros_pendentes(pasta, conn):
            try:
                numero_linhas = processar_ficheiro(ficheiro, conn)

                logger.info("Carreguei %d vendas de %s", numero_linhas, ficheiro.name)
                relatorio["processados"].append(ficheiro.name)

            except (KeyError, ValueError) as erro:
                logger.error("Erro ao processar %s: %s", ficheiro.name, erro)
                relatorio["falhados"].append(ficheiro.name)
                continue

        relatorio["linhas"] = contar(conn, "vendas")

    conn.close()
    return relatorio


# ---------------------------------------------------------------- Extensão (opcional)

def esquecer_ficheiro(nome: str, conn: sqlite3.Connection) -> None:
    """Retira um ficheiro de ficheiros_processados, para voltar a ser processado na próxima execução."""
    # EXTENSÃO: dentro de with conn:, DELETE FROM ficheiros_processados WHERE nome = ?
    with conn:
        conn.execute("DELETE FROM ficheiros_processados WHERE nome = ?", (nome,))


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Pipeline de vendas mensais da Morabeza")
    parser.add_argument("pasta")
    parser.add_argument("base_dados")
    args = parser.parse_args(argv)
    relatorio = correr(args.pasta, args.base_dados)
    print(f"Processados: {len(relatorio['processados'])}  Falhados: {len(relatorio['falhados'])}  "
          f"Vendas na base: {relatorio['linhas']}")
    return 1 if relatorio["falhados"] else 0


if __name__ == "__main__":
    sys.exit(main())
