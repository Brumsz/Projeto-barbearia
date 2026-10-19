import pytest
from decimal import Decimal
from datetime import datetime


from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from domain.agendamento import Agendamento
from domain.servico import Servico,TipoDeServico
from domain.pagamento import Pagamento,MetodoPagamento
from application.use_cases.registrar_pagamento import RegistrarPagamento



class RelogioFixo:
    def __init__(self, momento: datetime):
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento



def test_registrar_pagamento():

    servico = Servico(TipoDeServico.CABELO,Decimal("30.00"))
    agendamento = Agendamento('01','99d','2e',servico,datetime(2026, 10, 20, 9, 0))

    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)

    agendamento.registrar_pagamento(pagamento)

    assert agendamento.pagamento is pagamento


def test_registrar_pagamento_de_agendamento_cancelado():

    servico = Servico(TipoDeServico.CABELO,Decimal("30.00"))
    agendamento = Agendamento('01','99d','2e',servico,datetime(2026, 10, 20, 9, 0))
    agendamento.cancelar()

    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)
    
    with pytest.raises(ValueError, match="cancelado"):
        agendamento.registrar_pagamento(pagamento)


def test_registrar_pagamento_ja_registrado():
    
    servico = Servico(TipoDeServico.CABELO,Decimal("30.00"))
    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)
    agendamento = Agendamento('01','99d','2e',servico,datetime(2026, 10, 20, 9, 0),pagamento=pagamento)

    segundo_pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 10),MetodoPagamento.DINHEIRO)

    with pytest.raises(ValueError, match="ja registrado"):
        agendamento.registrar_pagamento(segundo_pagamento)


def test_registrar_pagamento_valor_diferente_do_servico():

    servico = Servico(TipoDeServico.CABELO,Decimal("30.00"))
    agendamento = Agendamento('01','99d','2e',servico,datetime(2026, 10, 20, 9, 0))

    pagamento = Pagamento(Decimal('20.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)

    with pytest.raises(ValueError, match="mesmo valor"):
        agendamento.registrar_pagamento(pagamento)


def test_registrar_pagamento_em_agendamento_criado():

    repositorio = RepositorioAgendamentoEmMemoria()
    caso = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))

    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)
    agendamento = caso.executar("01b", "02A", "12w", servico, datetime(2026, 10, 20, 9, 0))

    registro = RegistrarPagamento(repositorio).executar("01b",pagamento)

    assert repositorio.buscar("01b").pagamento is pagamento


def test_registrar_pagamento_em_agendamento_inexistente():

    repositorio = RepositorioAgendamentoEmMemoria()
    pagamento = Pagamento(Decimal('30.00'),datetime(2026, 10, 20, 9, 0),MetodoPagamento.DINHEIRO)

    with pytest.raises(ValueError, match='não encontrado' ):
        RegistrarPagamento(repositorio).executar("01b",pagamento)         