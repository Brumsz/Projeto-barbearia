from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum

class MetodoPagamento(Enum):
    PIX = "pix"
    DINHEIRO = "dinheiro"

class StatusPagamento(Enum):
    PENDENTE = "pendente"
    PAGO = "pago"

@dataclass
class Pagamento:
    valor: Decimal
    data: datetime
    metodo_de_pagamento: MetodoPagamento
    status: StatusPagamento = StatusPagamento.PENDENTE

    def __post_init__(self):
        if self.valor <= Decimal("0"):
            raise ValueError('O valor do pagamento deve ser maior que zero!')

    def confirmar_pagamento(self):
        self.status = StatusPagamento.PAGO