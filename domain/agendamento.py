from dataclasses import dataclass
from enum import Enum

from domain.servico import Servico
from domain.horario import Horario
from domain.pagamento import Pagamento
from domain.pagamento import StatusPagamento


class StatusAgendamento(Enum):
    ATIVO = "ativo"
    CANCELADO = "cancelado"

@dataclass
class Agendamento():
    id: str
    cliente_id:str
    barbeiro_id:str
    servico: Servico
    horario: Horario
    status: StatusAgendamento = StatusAgendamento.ATIVO
    pagamento: Pagamento | None = None

    def __post_init__(self):
        if not self.cliente_id or not self.barbeiro_id:
            raise ValueError('Agendamento precisa de um barbeiro e de um cliente')

    def cancelar(self) -> None:
        if self.pagamento is not None and self.pagamento.status == StatusPagamento.PAGO:
            raise ValueError('Não é possível cancelar um agendamento já pago')
        self.status = StatusAgendamento.CANCELADO


    