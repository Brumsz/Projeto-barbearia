import pytest
from datetime import datetime
from decimal import Decimal

from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from domain.servico import Servico,TipoDeServico
from application.use_cases.cancelar_agendamento import CancelarAgendamento
from domain.pagamento import Pagamento,StatusPagamento,MetodoPagamento
from domain.agendamento import Agendamento,StatusAgendamento

class RelogioFixo:
    def __init__(self, momento: datetime):
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento

def test_cancelar_agendamento():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso_agendar = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))

    agendar = caso_agendar.executar('01b','90a','2ea',TipoDeServico.CABELO,datetime(2026, 10, 20, 9, 0))

    caso_cancelar = CancelarAgendamento(repositorio)
    caso_cancelar.executar("01b")

    assert repositorio.buscar('01b').status == StatusAgendamento.CANCELADO

def test_cancelar_agendamento_nao_encontrado():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso_cancelar = CancelarAgendamento(repositorio)
    
    with pytest.raises(ValueError):
        caso_cancelar.executar("01b")

def test_cancelar_agendamento_pago():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso_agendar = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))
    
    agendar = caso_agendar.executar('02b','97a','9ea',TipoDeServico.CABELO,datetime(2026, 10, 20, 9, 0))

    agendamento = repositorio.buscar('02b')
    agendamento.pagamento = Pagamento(Decimal("30.00"), datetime(2026, 10, 20, 9, 0), MetodoPagamento.PIX)
    agendamento.pagamento.confirmar_pagamento()
        
    caso_cancelar = CancelarAgendamento(repositorio)

    with pytest.raises(ValueError):
        caso_cancelar.executar("02b")


def test_horario_cancelado_esta_disponivel():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso_agendar = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))

    agendar = caso_agendar.executar('01b','90a','2ea',TipoDeServico.CABELO,datetime(2026, 10, 20, 9, 0))

    caso_cancelar = CancelarAgendamento(repositorio)
    caso_cancelar.executar("01b")

    assert not repositorio.horario_ocupado('2ea',datetime(2026, 10, 20, 9, 0))