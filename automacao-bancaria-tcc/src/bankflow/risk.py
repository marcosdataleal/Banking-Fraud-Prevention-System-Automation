from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def calcular_score_risco(transacoes: pd.DataFrame) -> pd.DataFrame:
    df = transacoes.copy()

    df["valor_abs"] = df["valor"].abs()
    df["hora"] = pd.to_datetime(df["data_hora"]).dt.hour
    df["valor_acima_limite"] = df["valor"] > df["limite_diario"].fillna(0)
    df["conta_invalida"] = df["status_conta"].isna()
    df["conta_bloqueada"] = df["status_conta"].isin(["BLOQUEADA", "ENCERRADA"])
    df["horario_sensivel"] = df["hora"].between(0, 5)

    df["duplicada"] = df.duplicated(
        subset=["account_id", "tipo", "valor", "data_hora", "canal"],
        keep=False,
    )

    df["score_regras"] = (
        df["valor_acima_limite"].astype(int) * 30
        + df["conta_invalida"].astype(int) * 35
        + df["conta_bloqueada"].astype(int) * 30
        + df["horario_sensivel"].astype(int) * 10
        + df["duplicada"].astype(int) * 18
        + df["perfil_risco_cliente"].map({"BAIXO": 0, "MEDIO": 8, "ALTO": 18}).fillna(25)
    )

    df["score_anomalia"] = _score_anomalia(df)
    df["risk_score"] = np.clip(df["score_regras"] + df["score_anomalia"], 0, 100).round(2)
    df["nivel_risco"] = pd.cut(
        df["risk_score"],
        bins=[-1, 29, 59, 100],
        labels=["BAIXO", "MEDIO", "ALTO"],
    ).astype(str)
    return df.drop(columns=["valor_abs", "hora", "score_regras", "score_anomalia"])


def _score_anomalia(df: pd.DataFrame) -> np.ndarray:
    if len(df) < 20:
        return np.zeros(len(df))

    features = df[["valor", "tipo", "canal"]].copy()
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["valor"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["tipo", "canal"]),
        ]
    )
    model = IsolationForest(contamination=0.04, random_state=42)
    pipeline = Pipeline([("prep", preprocessor), ("model", model)])
    pipeline.fit(features)

    raw_scores = -pipeline.named_steps["model"].decision_function(
        pipeline.named_steps["prep"].transform(features)
    )
    normalized = (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-9)
    return normalized * 25
