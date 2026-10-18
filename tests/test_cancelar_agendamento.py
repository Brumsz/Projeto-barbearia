import pytest
from datetime import datetime
from decimal import Decimal

from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from domain.servico import Servico,TipoDeServico
from application.use_cases.cancelar_agendamento import CancelarAgendamento
from domain.horario import Horario
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
    cancelar = caso_cancelar.executar("01b")

    assert repositorio.buscar('01b').status == StatusAgendamento.CANCELADO

    
    

    
