from pathlib import Path


PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
DB_DIR = DATA_DIR / "database"

ACCOUNTS_FILE = INPUT_DIR / "contas.csv"
TRANSACTIONS_FILE = INPUT_DIR / "transacoes.csv"

PROCESSED_FILE = OUTPUT_DIR / "transacoes_processadas.csv"
AUDIT_SAMPLE_FILE = OUTPUT_DIR / "amostra_auditoria.csv"
METRICS_FILE = OUTPUT_DIR / "indicadores.json"
HTML_REPORT_FILE = OUTPUT_DIR / "relatorio_auditoria.html"
DATABASE_FILE = DB_DIR / "bankflow.sqlite"


def ensure_directories() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
