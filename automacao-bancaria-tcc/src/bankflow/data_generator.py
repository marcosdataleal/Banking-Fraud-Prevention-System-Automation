from __future__ import annotations

from datetime import datetime, timedelta
from random import Random

import numpy as np
import pandas as pd

from bankflow.config import ACCOUNTS_FILE, TRANSACTIONS_FILE, ensure_directories


TIPOS_TRANSACAO = ["PIX", "TED", "BOLETO", "CARTAO", "SAQUE", "DEPOSITO"]
STATUS_CONTA = ["ATIVA", "BLOQUEADA", "ENCERRADA"]
NOMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Gabriela", "Henrique",
    "Isabela", "Joao", "Larissa", "Marcos", "Natalia", "Otavio", "Patricia", "Rafael",
]
SOBRENOMES = [
    "Almeida", "Barbosa", "Costa", "Dias", "Ferreira", "Gomes", "Lima", "Martins",
    "Oliveira", "Pereira", "Ribeiro", "Rocha", "Santos", "Silva", "Souza", "Teixeira",
]


def gerar_contas(qtd_contas: int = 100, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    contas = []
    for indice in range(qtd_contas):
        contas.append(
            {
                "account_id": f"ACC{indice + 1:05d}",
                "cliente": _gerar_nome(rng),
                "cpf": _gerar_cpf_sintetico(rng),
                "agencia": rng.integers(1000, 9999),
                "saldo_inicial": round(float(rng.lognormal(mean=8.2, sigma=0.9)), 2),
                "status_conta": rng.choice(STATUS_CONTA, p=[0.88, 0.08, 0.04]),
                "perfil_risco_cliente": rng.choice(["BAIXO", "MEDIO", "ALTO"], p=[0.68, 0.24, 0.08]),
                "limite_diario": round(float(rng.uniform(1500, 25000)), 2),
            }
        )
    return pd.DataFrame(contas)


def gerar_transacoes(
    contas: pd.DataFrame,
    qtd_transacoes: int = 2000,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 1)
    random = Random(seed)
    account_ids = contas["account_id"].to_list()
    datas = [
        datetime.now() - timedelta(days=int(rng.integers(0, 90)), minutes=int(rng.integers(0, 1440)))
        for _ in range(qtd_transacoes)
    ]

    transacoes = []
    for indice in range(qtd_transacoes):
        tipo = rng.choice(TIPOS_TRANSACAO, p=[0.36, 0.12, 0.18, 0.18, 0.08, 0.08])
        valor = round(float(rng.lognormal(mean=6.4, sigma=1.05)), 2)

        if random.random() < 0.025:
            valor *= random.randint(8, 25)

        account_id = random.choice(account_ids)
        if random.random() < 0.012:
            account_id = f"ACCX{random.randint(10000, 99999)}"

        destino_id = random.choice(account_ids)
        if tipo in ["SAQUE", "DEPOSITO", "CARTAO", "BOLETO"]:
            destino_id = ""

        transacoes.append(
            {
                "transaction_id": f"TRX{indice + 1:07d}",
                "account_id": account_id,
                "destino_id": destino_id,
                "tipo": tipo,
                "valor": round(valor, 2),
                "data_hora": datas[indice].isoformat(timespec="seconds"),
                "canal": rng.choice(["APP", "INTERNET_BANKING", "CAIXA", "ATM"], p=[0.52, 0.26, 0.08, 0.14]),
            }
        )

    df = pd.DataFrame(transacoes)

    duplicadas = df.sample(frac=0.01, random_state=seed).copy()
    duplicadas["transaction_id"] = [f"DUP{i + 1:07d}" for i in range(len(duplicadas))]
    return pd.concat([df, duplicadas], ignore_index=True)


def salvar_dados(qtd_contas: int = 100, qtd_transacoes: int = 2000, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_directories()
    contas = gerar_contas(qtd_contas=qtd_contas, seed=seed)
    transacoes = gerar_transacoes(contas=contas, qtd_transacoes=qtd_transacoes, seed=seed)

    contas.to_csv(ACCOUNTS_FILE, index=False)
    transacoes.to_csv(TRANSACTIONS_FILE, index=False)
    return contas, transacoes


def _gerar_nome(rng: np.random.Generator) -> str:
    return f"{rng.choice(NOMES)} {rng.choice(SOBRENOMES)}"


def _gerar_cpf_sintetico(rng: np.random.Generator) -> str:
    digitos = "".join(str(int(rng.integers(0, 10))) for _ in range(11))
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
