from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineResult:
    total_transacoes: int
    aprovadas: int
    rejeitadas: int
    valor_total: float
    valor_aprovado: float
    taxa_rejeicao: float
    risco_medio: float
    amostras_auditoria: int
