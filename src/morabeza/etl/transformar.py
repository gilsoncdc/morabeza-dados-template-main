"""Lab 5 · Transformar (limpar) as vendas com funções puras.

Função pura = não altera o que recebe e devolve sempre o mesmo para a mesma
entrada. Testa com:
    pytest tests/test_etl_lab5.py -v
"""

import unicodedata

import pandas as pd

ILHAS_VALIDAS = ["Santiago", "São Vicente", "Sal", "Boa Vista", "Fogo", "Santo Antão"]

# abreviaturas que aparecem nos dados (chave já "achatada")
_ALIASES = {
    "stgo": "Santiago",
    "sv": "São Vicente",
    "svicente": "São Vicente",
    "boavista": "Boa Vista",
    "santao": "Santo Antão",
}


def _achatar(texto):
    """(VEM PRONTA) 'S. Vicente ' -> 'svicente' (minúsculas, sem acentos,
    só letras e números)."""
    sem_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return "".join(ch for ch in sem_acentos.lower() if ch.isalnum())


_CANON = {_achatar(i): i for i in ILHAS_VALIDAS} | _ALIASES


def normalizar_ilha(texto):
    """'  SAO vicente' -> 'São Vicente'. Ilha não servida, vazia ou None -> None.
    Dica: _CANON.get(_achatar(...))"""
    if pd.isna(texto):
        return None

    return _CANON.get(_achatar(str(texto)))


def normalizar_data(texto):
    """Aceita '2025-03-01' e '01/03/2025'. Devolve pd.Timestamp; data
    impossível ou vazia -> pd.NaT. Dica: pd.to_datetime(..., format=..., errors="coerce")"""
    if pd.isna(texto):
        return pd.NaT

    if "/" in texto:
        formato = "%d/%m/%Y"
    else:
        formato = "%Y-%m-%d"

    data = pd.to_datetime(texto, format=formato, errors="coerce")

    return data

def limpar_numero(serie):
    """(VEM PRONTA) '12 un' -> 12.0, '1250 CVE' -> 1250.0, '' -> NaN.
    A expressão regular apanha o primeiro número (com casas decimais opcionais)."""
    return (serie.astype("string")
                 .str.extract(r"(\d+(?:[.,]\d+)?)", expand=False)
                 .str.replace(",", ".", regex=False)
                 .astype(float))


def remover_duplicados(df):
    """Remove linhas com venda_id repetido (fica a primeira)."""
    return df.drop_duplicates(subset=["venda_id"])


def limpar_vendas(df):
    """Junta tudo. NÃO altera o df original (usa .assign ou .copy()).
    Passos:
      1. remover duplicados
      2. normalizar ilha e data; limpar quantidade e preco_unitario
      3. remover linhas onde algum destes quatro ficou vazio
      4. quantidade e preco_unitario como int
    """
    df=df.copy()
    
    out = remover_duplicados(df)
    out = out.assign(
        ilha=out["ilha"].map(normalizar_ilha),
        data=out["data"].map(normalizar_data),
        quantidade=limpar_numero(out["quantidade"]),
        preco_unitario=limpar_numero(out["preco_unitario"]),
    )
    out = out.dropna(subset=["ilha", "data", "quantidade", "preco_unitario"])
    out = out.astype({"quantidade": int, "preco_unitario": int})
    return out.reset_index(drop=True)


if __name__ == "__main__":
    print(pd.__version__)
