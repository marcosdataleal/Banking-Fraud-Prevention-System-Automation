# Arquitetura do Projeto

## Visao geral

O BankFlow Auditor foi organizado em camadas simples para facilitar manutencao, apresentacao academica e evolucao futura.

```text
Dados sinteticos -> Conciliacao -> Analise de risco -> Amostragem -> Relatorios/API/Dashboard
```

## Camadas

### Geracao de dados

Arquivo principal: `src/bankflow/data_generator.py`

Cria contas e transacoes ficticias para demonstrar o problema sem usar dados reais de clientes.

### Regras bancarias

Arquivo principal: `src/bankflow/services.py`

Valida transacoes com regras como conta inexistente, conta bloqueada, valor invalido e saldo insuficiente.

### Analise de risco

Arquivo principal: `src/bankflow/risk.py`

Combina regras de negocio com deteccao de anomalias usando `IsolationForest`, gerando uma pontuacao de risco entre 0 e 100.

### Amostragem

Arquivo principal: `src/bankflow/sampling.py`

Seleciona uma amostra de auditoria combinando transacoes rejeitadas, alto risco e amostragem estratificada.

### Persistencia

Arquivo principal: `src/bankflow/database.py`

Salva contas, transacoes processadas, amostras e indicadores em SQLite.

### API

Arquivo principal: `src/bankflow/api.py`

Expoe consultas para indicadores, transacoes e amostras de auditoria.

### Dashboard

Arquivo principal: `dashboard.py`

Permite visualizar indicadores, graficos, filtros e tabelas de auditoria.

## Beneficio pratico

O sistema reduz o esforco de revisao manual, prioriza casos sensiveis e cria uma base rastreavel para auditoria, compliance e operacoes financeiras.
