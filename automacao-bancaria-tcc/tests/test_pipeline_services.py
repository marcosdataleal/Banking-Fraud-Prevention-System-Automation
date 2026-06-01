import pandas as pd

from bankflow.services import conciliar_transacoes


def test_conciliacao_rejeita_conta_inexistente():
    contas = pd.DataFrame(
        {
            "account_id": ["ACC00001"],
            "saldo_inicial": [500.0],
            "status_conta": ["ATIVA"],
            "perfil_risco_cliente": ["BAIXO"],
            "limite_diario": [1000.0],
        }
    )
    transacoes = pd.DataFrame(
        {
            "transaction_id": ["TRX1"],
            "account_id": ["ACC99999"],
            "destino_id": [""],
            "tipo": ["PIX"],
            "valor": [100.0],
            "data_hora": ["2026-01-01T10:00:00"],
            "canal": ["APP"],
        }
    )

    resultado = conciliar_transacoes(contas, transacoes)

    assert resultado.loc[0, "status_processamento"] == "REJEITADA"
    assert resultado.loc[0, "motivo"] == "CONTA_INEXISTENTE"
