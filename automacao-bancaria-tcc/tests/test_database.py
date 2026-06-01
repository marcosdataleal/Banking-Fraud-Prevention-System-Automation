from pathlib import Path

import pandas as pd

from bankflow.database import carregar_tabela, obter_indicadores, salvar_resultados_sqlite


def test_salvar_e_ler_resultados_sqlite(tmp_path: Path):
    db_path = tmp_path / "bankflow.sqlite"
    contas = pd.DataFrame({"account_id": ["ACC1"], "saldo_inicial": [100.0]})
    transacoes = pd.DataFrame({"transaction_id": ["TRX1"], "account_id": ["ACC1"], "valor": [50.0]})
    processadas = pd.DataFrame(
        {
            "transaction_id": ["TRX1"],
            "nivel_risco": ["BAIXO"],
            "status_processamento": ["APROVADA"],
            "risk_score": [10.0],
        }
    )
    amostra = processadas.copy()
    indicadores = {"total_transacoes": 1, "risco_medio": 10.0}

    salvar_resultados_sqlite(contas, transacoes, processadas, amostra, indicadores, db_path=db_path)

    assert len(carregar_tabela("transacoes_processadas", db_path=db_path)) == 1
    assert obter_indicadores(db_path=db_path)["total_transacoes"] == 1
