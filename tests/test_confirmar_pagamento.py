import pytest
from datetime import datetime
from decimal import Decimal

from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from domain.agendamento import Agendamento,StatusPagamento
from domain.pagamento import Pagamento,MetodoPagamento
from domain.servico import Servico,TipoDeServico 
from application.use_cases.registrar_pagamento import RegistrarPagamento
from application.use_cases.confirmar_pagamento import ConfirmarPagamento



class RelogioFixo:
    def __init__(self, momento: datetime):
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento

    
def test_confirmar_pagamento():
    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    agendamento = Agendamento('01', '99d', '2e', servico, datetime(2026, 10, 20, 9, 0))
    pagamento = Pagamento(Decimal('30.00'), datetime(2026, 10, 20, 9, 0), MetodoPagamento.DINHEIRO)

    agendamento.registrar_pagamento(pagamento)
    assert pagamento.status == StatusPagamento.PENDENTE

    agendamento.confirmar_pagamento()

    assert agendamento.pagamento.status == StatusPagamento.PAGO


def test_confirmar_pagamento_em_agendamento_criado():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))

    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    agendamento = caso.executar("01b", "02A", "12w", servico, datetime(2026, 10, 20, 9, 0))
    
    pagamento = Pagamento(Decimal('30.00'), datetime(2026, 10, 20, 9, 0), MetodoPagamento.DINHEIRO)

    RegistrarPagamento(repositorio).executar('01b',pagamento)
    ConfirmarPagamento(repositorio).executar('01b')

    assert repositorio.buscar('01b').pagamento.status == StatusPagamento.PAGO


def test_confirmar_pagamento_em_agendamento_inexistente():

    repositorio = RepositorioAgendamentoEmMemoria()
    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)

    with pytest.raises(ValueError,match='não encontrado'):
        ConfirmarPagamento(repositorio).executar('01')


     

    

    

