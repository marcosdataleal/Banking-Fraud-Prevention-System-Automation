from __future__ import annotations

import pandas as pd


def conciliar_transacoes(contas: pd.DataFrame, transacoes: pd.DataFrame) -> pd.DataFrame:
    df = transacoes.merge(contas, on="account_id", how="left")
    df["motivo"] = "APROVADA"
    df["status_processamento"] = "APROVADA"

    conta_invalida = df["status_conta"].isna()
    conta_bloqueada = df["status_conta"].isin(["BLOQUEADA", "ENCERRADA"])
    valor_invalido = df["valor"] <= 0
    saldo_insuficiente = (
        ~conta_invalida
        & ~conta_bloqueada
        & df["tipo"].isin(["PIX", "TED", "BOLETO", "CARTAO", "SAQUE"])
        & (df["valor"] > df["saldo_inicial"].fillna(0))
    )

    df.loc[conta_invalida, ["status_processamento", "motivo"]] = ["REJEITADA", "CONTA_INEXISTENTE"]
    df.loc[conta_bloqueada, ["status_processamento", "motivo"]] = ["REJEITADA", "CONTA_BLOQUEADA_OU_ENCERRADA"]
    df.loc[valor_invalido, ["status_processamento", "motivo"]] = ["REJEITADA", "VALOR_INVALIDO"]
    df.loc[saldo_insuficiente, ["status_processamento", "motivo"]] = ["REJEITADA", "SALDO_INSUFICIENTE"]

    df["impacto_financeiro"] = df["valor"].where(df["status_processamento"] == "APROVADA", 0.0)
    return df


def calcular_indicadores(df: pd.DataFrame, tamanho_amostra: int) -> dict:
    total = int(len(df))
    aprovadas = int((df["status_processamento"] == "APROVADA").sum())
    rejeitadas = total - aprovadas
    valor_total = float(df["valor"].sum())
    valor_aprovado = float(df["impacto_financeiro"].sum())

    return {
        "total_transacoes": total,
        "aprovadas": aprovadas,
        "rejeitadas": rejeitadas,
        "taxa_rejeicao": round(rejeitadas / total if total else 0, 4),
        "valor_total": round(valor_total, 2),
        "valor_aprovado": round(valor_aprovado, 2),
        "risco_medio": round(float(df["risk_score"].mean()), 2) if total else 0,
        "transacoes_alto_risco": int((df["nivel_risco"] == "ALTO").sum()),
        "amostras_auditoria": tamanho_amostra,
        "motivos_rejeicao": df[df["status_processamento"] == "REJEITADA"]["motivo"].value_counts().to_dict(),
    }
