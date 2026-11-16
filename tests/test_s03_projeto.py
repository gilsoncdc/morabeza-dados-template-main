"""Testes do laboratório da Sessão 3. Corre: pytest tests/test_s03_projeto.py -v"""
import logging
import shutil
import subprocess
from pathlib import Path

import pytest

from morabeza.cli import main
from morabeza.config import ConfigInvalida, carregar_config

RAIZ = Path(__file__).parent.parent
AMOSTRA = RAIZ / "data" / "vendas_amostra.csv"


@pytest.fixture
def config_teste(tmp_path):
    caminho = tmp_path / "config.yaml"
    caminho.write_text(f"ficheiro_vendas: {AMOSTRA}\nmoeda: CVE\n", encoding="utf-8")
    return str(caminho)


def test_carregar_config_le_o_yaml(config_teste):
    config = carregar_config(config_teste)
    assert config["moeda"] == "CVE"
    assert config["ficheiro_vendas"].endswith("vendas_amostra.csv")


def test_carregar_config_do_projeto():
    assert carregar_config(str(RAIZ / "config.yaml"))["moeda"] == "CVE"


def test_config_inexistente(tmp_path):
    with pytest.raises(ConfigInvalida):
        carregar_config(str(tmp_path / "nao_existe.yaml"))


def test_config_sem_chave_obrigatoria(tmp_path):
    caminho = tmp_path / "config.yaml"
    caminho.write_text("moeda: CVE\n", encoding="utf-8")
    with pytest.raises(ConfigInvalida, match="ficheiro_vendas"):
        carregar_config(str(caminho))


def test_cli_total(config_teste, capsys):
    assert main(["--config", config_teste]) == 0
    assert "Faturação total: 1530740 CVE" in capsys.readouterr().out


def test_cli_por_ilha(config_teste, capsys):
    assert main(["--config", config_teste, "--ilha", "Sal"]) == 0
    assert "Faturação em Sal: 226410 CVE" in capsys.readouterr().out


def test_cli_ilha_desconhecida(config_teste):
    assert main(["--config", config_teste, "--ilha", "Brava"]) == 1


def test_cli_regista_no_log(config_teste, caplog):
    with caplog.at_level(logging.INFO):
        main(["--config", config_teste])
    assert any("300 vendas" in r.getMessage() for r in caplog.records), "usa logger.info para a contagem"


def test_legado_passa_no_ruff():
    ruff = shutil.which("ruff")
    if ruff is None:
        pytest.fail("o ruff não está instalado: corre pip install -e \".[dev,dados]\"")
    resultado = subprocess.run([ruff, "check", str(RAIZ / "src" / "morabeza" / "legado.py")],
                               capture_output=True, text=True, check=False)
    assert resultado.returncode == 0, resultado.stdout
