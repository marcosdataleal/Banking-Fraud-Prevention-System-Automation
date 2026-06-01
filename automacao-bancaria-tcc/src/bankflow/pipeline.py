from __future__ import annotations

import json

import pandas as pd

from bankflow.config import (
    ACCOUNTS_FILE,
    AUDIT_SAMPLE_FILE,
    HTML_REPORT_FILE,
    METRICS_FILE,
    PROCESSED_FILE,
    TRANSACTIONS_FILE,
    ensure_directories,
)
from bankflow.database import salvar_resultados_sqlite
from bankflow.risk import calcular_score_risco
from bankflow.sampling import selecionar_amostra_auditoria
from bankflow.services import calcular_indicadores, conciliar_transacoes


def executar_pipeline() -> dict:
    ensure_directories()
    contas = pd.read_csv(ACCOUNTS_FILE)
    transacoes = pd.read_csv(TRANSACTIONS_FILE)

    conciliadas = conciliar_transacoes(contas, transacoes)
    com_risco = calcular_score_risco(conciliadas)
    amostra = selecionar_amostra_auditoria(com_risco)
    indicadores = calcular_indicadores(com_risco, tamanho_amostra=len(amostra))

    com_risco.to_csv(PROCESSED_FILE, index=False)
    amostra.to_csv(AUDIT_SAMPLE_FILE, index=False)
    METRICS_FILE.write_text(json.dumps(indicadores, indent=2, ensure_ascii=False), encoding="utf-8")
    HTML_REPORT_FILE.write_text(_gerar_html(indicadores, amostra), encoding="utf-8")
    salvar_resultados_sqlite(contas, transacoes, com_risco, amostra, indicadores)

    return indicadores


def _gerar_html(indicadores: dict, amostra: pd.DataFrame) -> str:
    top_amostras = amostra.head(20)[
        ["transaction_id", "account_id", "tipo", "valor", "risk_score", "nivel_risco", "motivo"]
    ].to_html(index=False, classes="table")
    por_risco = amostra["nivel_risco"].value_counts().to_dict()
    risco_cards = "".join(f"<li><strong>{risco}</strong><span>{qtd} transacoes</span></li>" for risco, qtd in por_risco.items())

    cards = "".join(
        f"<article><span>{chave.replace('_', ' ').title()}</span><strong>{valor}</strong></article>"
        for chave, valor in indicadores.items()
        if not isinstance(valor, dict)
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Relatorio BankFlow Auditor</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f4f7f9; color: #1f2933; }}
    header {{ background: #0b5c56; color: white; padding: 32px 48px; }}
    main {{ padding: 32px 48px; }}
    section.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 16px; }}
    article {{ background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 18px; }}
    article span {{ display: block; color: #52606d; font-size: 13px; margin-bottom: 8px; }}
    article strong {{ font-size: 24px; }}
    .panel {{ margin-top: 28px; background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 22px; overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #e4e7eb; padding: 10px; text-align: left; font-size: 14px; }}
    th {{ background: #f0f4f8; }}
    ul.risk {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; padding: 0; list-style: none; }}
    ul.risk li {{ background: #eef8f6; border: 1px solid #bfddd8; border-radius: 8px; padding: 14px; }}
    ul.risk strong, ul.risk span {{ display: block; }}
  </style>
</head>
<body>
  <header>
    <h1>BankFlow Auditor</h1>
    <p>Automacao bancaria com conciliacao, risco e amostragem para auditoria.</p>
  </header>
  <main>
    <section class="metrics">{cards}</section>
    <section class="panel">
      <h2>Amostras por nivel de risco</h2>
      <ul class="risk">{risco_cards}</ul>
    </section>
    <section class="panel">
      <h2>Top 20 transacoes selecionadas para auditoria</h2>
      {top_amostras}
    </section>
  </main>
</body>
</html>"""
