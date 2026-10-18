from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class TipoDeServico(Enum):
    CABELO = 'cabelo'
    BARBA = 'barba'

@dataclass(frozen=True)
class Servico:
    servico: TipoDeServico
    preco:Decimal

    def __post_init__(self):
        if self.preco <= Decimal("0"):
            raise ValueError('Preço do serviço tem que ser maior que zero!')
    