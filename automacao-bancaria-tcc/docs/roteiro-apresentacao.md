# Roteiro de Apresentacao

## 1. Problema

Empresas financeiras processam muitas transacoes diariamente. Conferir tudo manualmente e inviavel.

## 2. Proposta

Criar uma automacao em Python que valide transacoes, calcule risco e selecione amostras para auditoria.

## 3. Como funciona

1. O sistema gera dados sinteticos de contas e transacoes.
2. As transacoes passam por regras de conciliacao.
3. Cada transacao recebe uma pontuacao de risco.
4. O sistema separa casos rejeitados e de alto risco.
5. Uma amostra estatistica e criada para auditoria.
6. Os resultados ficam disponiveis em arquivos, banco SQLite, API e dashboard.

## 4. Tecnologias

- Python
- pandas
- numpy
- scikit-learn
- SQLite
- FastAPI
- Streamlit
- Plotly
- HTML/CSS

## 5. Resultado esperado

Reduzir trabalho manual, priorizar transacoes relevantes e apoiar areas de auditoria, compliance e backoffice financeiro.

## 6. Melhorias futuras

- Integrar com banco PostgreSQL.
- Criar autenticacao de usuarios.
- Receber arquivos de transacoes reais anonimizadas.
- Implantar a API e o dashboard em nuvem.
