from datetime import datetime
import pytest

from adapters.saida.memoria.repositorio_memoria import RepositorioAgendamentoEmMemoria
from adapters.saida.memoria.repositorio_servicos_memoria import  RepositorioServicosEmMemoria
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
    servicos = RepositorioServicosEmMemoria([Servico(TipoDeServico.BARBA, Decimal("20.00"))])
    caso = AgendarHorario(repositorio, RelogioFixo(datetime(2026, 10, 1, 8, 0)),servicos)

    agendamento = caso.executar("01b", "02A", "12w", TipoDeServico.BARBA , datetime(2026, 10, 20, 9, 0))

    assert agendamento.id == '01b'
    assert len(repositorio.agendamentos) == 1

def test_nao_agenda_no_passado():
    relogio = RelogioFixo(datetime(2026, 10, 21, 8, 0))
    repositorio = RepositorioAgendamentoEmMemoria()
    servicos = RepositorioServicosEmMemoria([Servico(TipoDeServico.BARBA, Decimal("20.00"))])
    caso = AgendarHorario(repositorio, relogio,servicos) 

    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))           

    with pytest.raises(ValueError):                     
        caso.executar("a1", "c1", "b1", TipoDeServico.BARBA, datetime(2026, 10, 20, 9, 0))  


def test_agendar_usa_preco_do_cadastro():
    repo = RepositorioAgendamentoEmMemoria()
    servicos = RepositorioServicosEmMemoria([Servico(TipoDeServico.BARBA, Decimal("20.00"))])
    caso = AgendarHorario(repo, RelogioFixo(datetime(2026, 10, 1, 8, 0)), servicos)

    agendamento = caso.executar("01", "c1", "b1", TipoDeServico.BARBA, datetime(2026, 10, 20, 9, 0))

    assert agendamento.servico.preco == Decimal("20.00")


def test_agendar_servico_nao_cadastrado_lanca_erro():
    repo = RepositorioAgendamentoEmMemoria()
    servicos = RepositorioServicosEmMemoria([])
    caso = AgendarHorario(repo, RelogioFixo(datetime(2026, 10, 1, 8, 0)), servicos)

    with pytest.raises(ValueError, match="não cadastrado"):
        caso.executar("01", "c1", "b1", TipoDeServico.BARBA, datetime(2026, 10, 20, 9, 0))