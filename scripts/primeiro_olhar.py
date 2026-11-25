"""Sessão 8 · Demo: primeiro olhar aos dados em bruto (antes de limpar).

    python scripts/primeiro_olhar.py
"""
import pandas as pd

df = pd.read_csv("data/fontes_s1_2025/vendas_s1_2025.csv", dtype=str)
print(df.shape)
print(df.sample(8, random_state=1), "\n")
print("Valores em falta por coluna:\n", df.isna().sum(), "\n")
print("venda_id repetidos:", df["venda_id"].duplicated().sum())
print("\nComo está escrita a ilha:\n", df["ilha"].value_counts())
print("\nDatas com /:", df["data"].str.contains("/").sum())
print("Quantidades que não são só dígitos:",
      (~df["quantidade"].fillna("").str.fullmatch(r"\d+")).sum())
print(df.loc[~df["quantidade"].fillna("").str.fullmatch(r"\d+"), "quantidade"].head(10).tolist())

# o que acontece se NÃO lermos como texto:
mau = pd.read_csv("data/fontes_s1_2025/vendas_s1_2025.csv")
print("\nSem dtype=str, quantidade é:", mau["quantidade"].dtype)
