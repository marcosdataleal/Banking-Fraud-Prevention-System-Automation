from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from bankflow.config import DATABASE_FILE, ensure_directories


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    ensure_directories()
    connection = sqlite3.connect(db_path or DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def salvar_resultados_sqlite(
    contas: pd.DataFrame,
    transacoes: pd.DataFrame,
    processadas: pd.DataFrame,
    amostra: pd.DataFrame,
    indicadores: dict,
    db_path: Path | None = None,
) -> None:
    with get_connection(db_path) as connection:
        contas.to_sql("contas", connection, if_exists="replace", index=False)
        transacoes.to_sql("transacoes_brutas", connection, if_exists="replace", index=False)
        processadas.to_sql("transacoes_processadas", connection, if_exists="replace", index=False)
        amostra.to_sql("amostra_auditoria", connection, if_exists="replace", index=False)

        indicadores_df = pd.DataFrame(
            [{"indicador": chave, "valor": str(valor)} for chave, valor in indicadores.items()]
        )
        indicadores_df.to_sql("indicadores", connection, if_exists="replace", index=False)

        _criar_indices(connection)


def carregar_tabela(nome: str, limite: int | None = None, db_path: Path | None = None) -> pd.DataFrame:
    permitidas = {"contas", "transacoes_brutas", "transacoes_processadas", "amostra_auditoria", "indicadores"}
    if nome not in permitidas:
        raise ValueError(f"Tabela nao permitida: {nome}")

    query = f"SELECT * FROM {nome}"
    if limite:
        query += f" LIMIT {int(limite)}"

    with get_connection(db_path) as connection:
        return pd.read_sql_query(query, connection)


def obter_indicadores(db_path: Path | None = None) -> dict:
    with get_connection(db_path) as connection:
        cursor = connection.execute("SELECT indicador, valor FROM indicadores")
        return {linha["indicador"]: _converter_valor(linha["valor"]) for linha in cursor.fetchall()}


def _criar_indices(connection: sqlite3.Connection) -> None:
    connection.execute("CREATE INDEX IF NOT EXISTS idx_processadas_risco ON transacoes_processadas(nivel_risco)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_processadas_status ON transacoes_processadas(status_processamento)")
    connection.execute("CREATE INDEX IF NOT EXISTS idx_amostra_risco ON amostra_auditoria(risk_score)")


def _converter_valor(valor: str) -> object:
    if valor.startswith("{") or valor.startswith("["):
        return valor
    try:
        numero = float(valor)
    except ValueError:
        return valor
    return int(numero) if numero.is_integer() else numero
