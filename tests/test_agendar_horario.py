from datetime import datetime
import pytest

from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from decimal import Decimal
from domain.servico import Servico, TipoDeServico

class RelogioFixo:
    def __init__(self, momento: datetime):
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento


def test_agendar_horario_livre():
    repositorio = RepositorioAgendamentoEmMemoria()
    caso = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)))

    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    agendamento = caso.executar("01b", "02A", "12w", servico, datetime(2026, 10, 20, 9, 0))

    assert agendamento.id == '01b'
    assert len(repositorio.agendamentos) == 1

def test_nao_agenda_no_passado():
    relogio = RelogioFixo(datetime(2026, 10, 21, 8, 0))
    repositorio = RepositorioAgendamentoEmMemoria()
    caso = AgendarHorario(repositorio, relogio) 

    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))           

    with pytest.raises(ValueError):                     
        caso.executar("a1", "c1", "b1", servico, datetime(2026, 10, 20, 9, 0))  

