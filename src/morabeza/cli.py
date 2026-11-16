"""Linha de comandos do projeto Morabeza (Sessão 3).

Uso:  python -m morabeza.cli --ilha Sal
"""
import argparse
import logging
import sys

from morabeza.apoio import faturacao_por_ilha, ler_vendas
from morabeza.config import carregar_config

logger = logging.getLogger(__name__)


def criar_parser() -> argparse.ArgumentParser:
    # TODO 5: cria um argparse.ArgumentParser com dois argumentos opcionais:
    #         --config (por defeito "config.yaml") e --ilha (sem valor por defeito).
    parser = argparse.ArgumentParser(
        description="Linha de comandos do projeto Morabeza"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Caminho do ficheiro de configuração"
    )
    parser.add_argument(
        "--ilha",
        help="Nome da ilha para calcular a faturação"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = criar_parser().parse_args(argv)

    # TODO 6: carrega a configuração (args.config) e lê as vendas do ficheiro indicado nela.
    # TODO 7: regista no log: logger.info("Li %d vendas de %s", ...). Não uses print para isto.
    # TODO 8: calcula a faturação por ilha. Sem --ilha, imprime "Faturação total: <valor> <moeda>".
    #         Com --ilha, imprime "Faturação em <ilha>: <valor> <moeda>".
    #         Se a ilha não existir, logger.error(...) e devolve 1. No fim, devolve 0.
    
    config = carregar_config(args.config)
    vendas = ler_vendas(config["ficheiro_vendas"])

    logger.info("Li %d vendas de %s", len(vendas), config["ficheiro_vendas"])

    faturacao = faturacao_por_ilha(vendas)
    moeda = config["moeda"]

    if args.ilha is None:
        total = sum(faturacao.values())
        print(f"Faturação total: {total} {moeda}")
    else:
        if args.ilha not in faturacao:
            logger.error("A ilha '%s' não existe.", args.ilha)
            return 1

        valor = faturacao[args.ilha]
        print(f"Faturação em {args.ilha}: {valor} {moeda}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
