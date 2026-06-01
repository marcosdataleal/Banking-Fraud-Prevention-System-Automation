from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from bankflow.database import carregar_tabela, obter_indicadores
from bankflow.pipeline import executar_pipeline


app = FastAPI(
    title="BankFlow Auditor API",
    description="API para consultar indicadores, transacoes e amostras de auditoria bancaria.",
    version="1.0.0",
)


@app.get("/")
def home() -> dict:
    return {
        "projeto": "BankFlow Auditor",
        "descricao": "Automacao bancaria com risco, auditoria e amostragem.",
        "docs": "/docs",
    }


@app.post("/executar")
def executar() -> dict:
    return executar_pipeline()


@app.get("/indicadores")
def indicadores() -> dict:
    try:
        return obter_indicadores()
    except Exception as exc:
        raise HTTPException(status_code=404, detail="Execute python main.py demo antes de consultar a API.") from exc


@app.get("/transacoes")
def transacoes(
    limite: int = Query(default=100, ge=1, le=1000),
    nivel_risco: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> list[dict]:
    df = carregar_tabela("transacoes_processadas")
    if nivel_risco:
        df = df[df["nivel_risco"].str.upper() == nivel_risco.upper()]
    if status:
        df = df[df["status_processamento"].str.upper() == status.upper()]
    return df.head(limite).to_dict(orient="records")


@app.get("/auditoria/amostras")
def amostras(limite: int = Query(default=100, ge=1, le=1000)) -> list[dict]:
    df = carregar_tabela("amostra_auditoria", limite=limite)
    return df.to_dict(orient="records")
