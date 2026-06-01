from __future__ import annotations

import math

import pandas as pd


def amostragem_estratificada(
    df: pd.DataFrame,
    coluna_estrato: str = "nivel_risco",
    frac: float = 0.12,
    minimo_por_estrato: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    amostras = []
    for _, grupo in df.groupby(coluna_estrato, dropna=False):
        tamanho = max(minimo_por_estrato, math.ceil(len(grupo) * frac))
        tamanho = min(tamanho, len(grupo))
        amostras.append(grupo.sample(n=tamanho, random_state=seed))

    resultado = pd.concat(amostras, ignore_index=True) if amostras else df.head(0)
    return resultado.sort_values(["risk_score", "valor"], ascending=False).reset_index(drop=True)


def amostragem_sistematica(df: pd.DataFrame, tamanho: int) -> pd.DataFrame:
    if tamanho <= 0 or df.empty:
        return df.head(0)

    ordenado = df.sort_values("data_hora").reset_index(drop=True)
    intervalo = max(len(ordenado) // tamanho, 1)
    return ordenado.iloc[::intervalo].head(tamanho).reset_index(drop=True)


def amostragem_aleatoria(df: pd.DataFrame, tamanho: int, seed: int = 42) -> pd.DataFrame:
    tamanho = min(max(tamanho, 0), len(df))
    return df.sample(n=tamanho, random_state=seed).reset_index(drop=True)


def selecionar_amostra_auditoria(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    alto_risco = df[df["nivel_risco"] == "ALTO"]
    rejeitadas = df[df["status_processamento"] == "REJEITADA"]
    estratificada = amostragem_estratificada(df, seed=seed)

    amostra = pd.concat([alto_risco, rejeitadas, estratificada], ignore_index=True)
    amostra = amostra.drop_duplicates(subset=["transaction_id"]).copy()
    amostra["prioridade_auditoria"] = pd.cut(
        amostra["risk_score"],
        bins=[-1, 39, 69, 100],
        labels=["NORMAL", "ATENCAO", "CRITICA"],
    ).astype(str)
    return amostra.sort_values(["prioridade_auditoria", "risk_score"], ascending=[True, False]).reset_index(drop=True)
