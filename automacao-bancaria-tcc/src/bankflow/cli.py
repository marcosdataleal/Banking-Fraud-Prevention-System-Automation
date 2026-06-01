from __future__ import annotations

import argparse
import json
import subprocess
import sys

from bankflow.config import (
    ACCOUNTS_FILE,
    AUDIT_SAMPLE_FILE,
    HTML_REPORT_FILE,
    PROCESSED_FILE,
    TRANSACTIONS_FILE,
)
from bankflow.data_generator import salvar_dados
from bankflow.pipeline import executar_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="BankFlow Auditor - automacao bancaria com amostragem")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    gerar = subparsers.add_parser("gerar-dados", help="Gera contas e transacoes sinteticas")
    gerar.add_argument("--qtd-contas", type=int, default=100)
    gerar.add_argument("--qtd-transacoes", type=int, default=2000)
    gerar.add_argument("--seed", type=int, default=42)

    subparsers.add_parser("executar", help="Executa conciliacao, risco, amostragem e relatorios")
    subparsers.add_parser("api", help="Inicia a API FastAPI em http://127.0.0.1:8000")
    subparsers.add_parser("dashboard", help="Inicia o dashboard Streamlit")

    demo = subparsers.add_parser("demo", help="Gera dados e executa toda a automacao")
    demo.add_argument("--qtd-contas", type=int, default=120)
    demo.add_argument("--qtd-transacoes", type=int, default=2500)
    demo.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.comando == "gerar-dados":
        salvar_dados(args.qtd_contas, args.qtd_transacoes, args.seed)
        print(f"Contas salvas em: {ACCOUNTS_FILE}")
        print(f"Transacoes salvas em: {TRANSACTIONS_FILE}")
        return

    if args.comando == "demo":
        salvar_dados(args.qtd_contas, args.qtd_transacoes, args.seed)

    if args.comando == "api":
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "bankflow.api:app", "--reload"],
            check=False,
        )
        return

    if args.comando == "dashboard":
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard.py"],
            check=False,
        )
        return

    indicadores = executar_pipeline()
    print(json.dumps(indicadores, indent=2, ensure_ascii=False))
    print(f"Transacoes processadas: {PROCESSED_FILE}")
    print(f"Amostra de auditoria: {AUDIT_SAMPLE_FILE}")
    print(f"Relatorio HTML: {HTML_REPORT_FILE}")


if __name__ == "__main__":
    main()
