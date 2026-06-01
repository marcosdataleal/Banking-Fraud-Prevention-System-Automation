# BankFlow Auditor - Automacao Bancaria com Auditoria Inteligente

Projeto em Python para automatizar rotinas de controle bancario, conciliacao de transacoes, classificacao de risco, selecao de amostras para auditoria, API e dashboard interativo. A proposta e simular um fluxo realista de backoffice bancario que poderia ser usado como base de TCC, portfolio ou prova de conceito.

## Dor de mercado

Bancos, fintechs e financeiras processam grandes volumes de transacoes todos os dias. Auditar tudo manualmente e caro, lento e sujeito a erro humano. O BankFlow Auditor atua como uma primeira camada automatizada: valida transacoes, calcula risco, separa casos suspeitos e entrega uma amostra priorizada para auditoria.

## Solucao proposta

O sistema cria uma base sintetica de contas e transacoes, executa regras de conciliacao, aplica deteccao de anomalias, salva tudo em SQLite, gera arquivos de saida, expoe uma API e entrega um dashboard para exploracao dos resultados.

## O que o projeto faz

- Gera uma base sintetica de transacoes bancarias.
- Processa as transacoes com regras de negocio.
- Calcula indicadores de risco por transacao.
- Identifica inconsistencias como saldo insuficiente, conta inexistente, valor suspeito e transacoes duplicadas.
- Salva resultados em banco de dados SQLite.
- Expoe endpoints com FastAPI.
- Mostra indicadores e graficos em dashboard Streamlit.
- Aplica tecnicas de amostragem para auditoria:
  - amostragem estratificada por nivel de risco;
  - amostragem sistematica;
  - amostragem aleatoria simples.
- Gera relatorios em `CSV`, `JSON` e `HTML`.
- Possui testes automatizados com `pytest`.

## Estrutura

```text
automacao-bancaria-tcc/
  data/
    input/
    output/
    database/
  docs/
  dashboard.py
  main.py
  src/
    bankflow/
      api.py
      __init__.py
      cli.py
      config.py
      data_generator.py
      database.py
      models.py
      pipeline.py
      risk.py
      sampling.py
      services.py
  tests/
  requirements.txt
  pyproject.toml
  README.md
```

## Tecnologias

- Python 3.10+
- pandas
- numpy
- scikit-learn
- FastAPI
- Uvicorn
- Streamlit
- Plotly
- SQLite
- pytest

## Como instalar

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
pip install -e .
```

## Como executar

Gerar dados sinteticos:

```bash
python -m bankflow.cli gerar-dados --qtd-contas 120 --qtd-transacoes 2500
```

Executar a automacao completa:

```bash
python -m bankflow.cli executar
```

Executar tudo em um unico comando:

```bash
python -m bankflow.cli demo
```

Se preferir, tambem da para rodar pelo arquivo principal:

```bash
python main.py demo
```

Os arquivos finais serao criados em:

```text
data/output/
```

Tambem sera criado um banco local em:

```text
data/database/bankflow.sqlite
```

## Abrir o dashboard

Depois de executar o demo, rode:

```bash
python main.py dashboard
```

Ou diretamente:

```bash
streamlit run dashboard.py
```

O navegador abrira um painel com indicadores, graficos, filtros, transacoes e amostras de auditoria.

## Iniciar a API

Depois de executar o demo, rode:

```bash
python main.py api
```

Acesse:

```text
http://127.0.0.1:8000/docs
```

Endpoints principais:

- `GET /indicadores`
- `GET /transacoes`
- `GET /transacoes?nivel_risco=ALTO`
- `GET /auditoria/amostras`
- `POST /executar`

## Relatorios gerados

- `transacoes_processadas.csv`: todas as transacoes com status, risco e motivo.
- `amostra_auditoria.csv`: amostra selecionada para auditoria.
- `indicadores.json`: indicadores agregados da execucao.
- `relatorio_auditoria.html`: relatorio visual simples para apresentar.
- `data/database/bankflow.sqlite`: banco com contas, transacoes, indicadores e amostras.

## Rodar testes

```bash
pytest
```

## Ideia de TCC

Tema sugerido:

> Automacao de processos bancarios com analise de risco e amostragem estatistica para auditoria de transacoes financeiras.

Problema:

Instituicoes financeiras lidam diariamente com grande volume de transacoes. Auditar tudo manualmente e caro, lento e sujeito a falhas. O projeto propoe automatizar a conciliacao e priorizar transacoes relevantes para auditoria usando regras de risco e tecnicas de amostragem.

Hipotese:

Uma automacao baseada em regras, indicadores de risco e amostragem estratificada pode reduzir o volume analisado manualmente sem perder foco nas transacoes mais criticas.

## Observacao importante

Este projeto usa dados sinteticos e nao acessa bancos reais. Ele foi desenhado para fins educacionais, portfolio e demonstracao tecnica.

## Proximos passos possiveis

- Conectar com PostgreSQL.
- Adicionar autenticacao na API.
- Criar historico de execucoes.
- Receber transacoes por upload ou endpoint.
- Implantar dashboard em nuvem.
