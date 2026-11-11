# Morabeza Dados

Repositório de trabalho do módulo **Engenharia de Software e Python para Dados** (Skodji Digital, Upskilling).

A Morabeza Distribuição é uma empresa fictícia que distribui produtos alimentares e de limpeza
por seis ilhas de Cabo Verde. Ao longo do módulo vais transformar os dados de vendas desta empresa
num pequeno produto de dados: leitura, limpeza, validação, testes e modelos.

## Preparar o ambiente (uma vez)

```bash
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificar o teu trabalho

```bash
pytest -v
```

## Obter os ficheiros de uma sessão nova

No início de cada sessão (a partir da Sessão 2), no terminal:

```bash
bash obter_sessao.sh 2      # troca 2 pelo número da sessão
```

## Correr o resumo de vendas

```bash
python -m morabeza.resumo data/vendas_amostra.csv
```
