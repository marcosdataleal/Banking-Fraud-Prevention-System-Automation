import pandas as pd

from bankflow.sampling import amostragem_estratificada, selecionar_amostra_auditoria


def test_amostragem_estratificada_preserva_estratos():
    df = pd.DataFrame(
        {
            "transaction_id": [f"T{i}" for i in range(30)],
            "nivel_risco": ["BAIXO"] * 10 + ["MEDIO"] * 10 + ["ALTO"] * 10,
            "risk_score": list(range(30)),
            "valor": [100.0] * 30,
        }
    )

    amostra = amostragem_estratificada(df, frac=0.2, minimo_por_estrato=2)

    assert set(amostra["nivel_risco"]) == {"BAIXO", "MEDIO", "ALTO"}
    assert len(amostra) == 6


def test_selecionar_amostra_prioriza_alto_risco_e_rejeitadas():
    df = pd.DataFrame(
        {
            "transaction_id": ["A", "B", "C", "D"],
            "nivel_risco": ["ALTO", "BAIXO", "MEDIO", "BAIXO"],
            "risk_score": [90, 10, 55, 20],
            "valor": [1000, 20, 300, 80],
            "status_processamento": ["APROVADA", "REJEITADA", "APROVADA", "APROVADA"],
        }
    )

    amostra = selecionar_amostra_auditoria(df)

    assert "A" in amostra["transaction_id"].to_list()
    assert "B" in amostra["transaction_id"].to_list()
    assert "prioridade_auditoria" in amostra.columns
