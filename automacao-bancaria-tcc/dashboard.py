from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import pandas as pd
import plotly.express as px
import streamlit as st

from bankflow.config import DATABASE_FILE
from bankflow.database import carregar_tabela, obter_indicadores
from bankflow.pipeline import executar_pipeline


st.set_page_config(page_title="BankFlow Auditor", layout="wide")

st.title("BankFlow Auditor")
st.caption("Painel de automacao bancaria, risco e auditoria.")

if st.sidebar.button("Executar automacao"):
    executar_pipeline()
    st.sidebar.success("Automacao executada com sucesso.")

if not DATABASE_FILE.exists():
    st.warning("Execute `python main.py demo` ou clique em `Executar automacao` para criar a base.")
    st.stop()

indicadores = obter_indicadores()
transacoes = carregar_tabela("transacoes_processadas")
amostra = carregar_tabela("amostra_auditoria")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Transacoes", indicadores.get("total_transacoes", 0))
col2.metric("Rejeitadas", indicadores.get("rejeitadas", 0))
col3.metric("Risco medio", indicadores.get("risco_medio", 0))
col4.metric("Amostras auditoria", indicadores.get("amostras_auditoria", 0))

st.sidebar.header("Filtros")
riscos = sorted(transacoes["nivel_risco"].dropna().unique().tolist())
status = sorted(transacoes["status_processamento"].dropna().unique().tolist())
risco_sel = st.sidebar.multiselect("Nivel de risco", riscos, default=riscos)
status_sel = st.sidebar.multiselect("Status", status, default=status)

filtrado = transacoes[
    transacoes["nivel_risco"].isin(risco_sel)
    & transacoes["status_processamento"].isin(status_sel)
].copy()

aba_visao, aba_transacoes, aba_auditoria = st.tabs(["Visao geral", "Transacoes", "Auditoria"])

with aba_visao:
    c1, c2 = st.columns(2)
    with c1:
        por_risco = filtrado["nivel_risco"].value_counts().reset_index()
        por_risco.columns = ["nivel_risco", "quantidade"]
        st.plotly_chart(px.bar(por_risco, x="nivel_risco", y="quantidade", title="Transacoes por risco"), use_container_width=True)
    with c2:
        por_tipo = filtrado.groupby("tipo", as_index=False)["valor"].sum()
        st.plotly_chart(px.pie(por_tipo, names="tipo", values="valor", title="Valor por tipo de transacao"), use_container_width=True)

    motivos = filtrado[filtrado["status_processamento"] == "REJEITADA"]["motivo"].value_counts().reset_index()
    motivos.columns = ["motivo", "quantidade"]
    st.plotly_chart(px.bar(motivos, x="motivo", y="quantidade", title="Motivos de rejeicao"), use_container_width=True)

with aba_transacoes:
    st.dataframe(
        filtrado[["transaction_id", "account_id", "tipo", "valor", "status_processamento", "motivo", "risk_score", "nivel_risco"]],
        use_container_width=True,
        hide_index=True,
    )

with aba_auditoria:
    st.dataframe(
        amostra[["transaction_id", "account_id", "tipo", "valor", "risk_score", "nivel_risco", "prioridade_auditoria", "motivo"]],
        use_container_width=True,
        hide_index=True,
    )
