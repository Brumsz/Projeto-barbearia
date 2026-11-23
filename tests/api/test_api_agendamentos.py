from fastapi.testclient import TestClient
from decimal import Decimal
from datetime import datetime

from adapters.entrada.api.app import criar_app
from adapters.saida.memoria.repositorio_memoria import RepositorioAgendamentoEmMemoria
from adapters.saida.memoria.repositorio_servicos_memoria import RepositorioServicosEmMemoria
from application.use_cases.agendar_horario import AgendarHorario
from domain.servico import TipoDeServico,Servico

class RelogioFixo:
    def __init__(self, momento: datetime):
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento

def casos_de_uso():

    repositorio = RepositorioAgendamentoEmMemoria()
    servicos = RepositorioServicosEmMemoria([Servico(TipoDeServico.BARBA, Decimal("20.00"))])

    return {'agendar' : AgendarHorario(repositorio,RelogioFixo(datetime(2026, 11, 18, 8, 0)),servicos)}


def test_post_agendamento_devolve_201_e_o_corpo():
    
    cliente_teste = TestClient(criar_app(casos_de_uso()))
    resposta = cliente_teste.post('/agendamentos',json={
        'id' : '1a',
        'cliente_id' : 'c1',
        'barbeiro_id' : 'b1',
        'tipo' : 'barba',
        'inicio' : '2026-11-20T09:00:00'
    })

    corpo = resposta.json()
    print(corpo)

    assert resposta.status_code == 201
    assert corpo['id'] == '1a'
    assert corpo['tipo'] == 'barba'
    assert corpo['status'] == 'ativo'
    assert corpo['preco'] == '20.00'


def test_post_agendamento_mesmo_horario():
    cliente_teste = TestClient(criar_app(casos_de_uso()))
    agendamento1 = cliente_teste.post('/agendamentos',json={
        'id' : '1a',
        'cliente_id' : 'c1',
        'barbeiro_id' : 'b1',
        'tipo' : 'barba',
        'inicio' : '2026-11-20T09:00:00'
    })

    assert agendamento1.status_code == 201

    agendamento2 = cliente_teste.post('/agendamentos',json={
        'id' : '2a',
        'cliente_id' : 'c2',
        'barbeiro_id' : 'b1',
        'tipo' : 'barba',
        'inicio' : '2026-11-20T09:00:00'
    })

    assert agendamento2.status_code == 409
    assert 'Horário Indisponivel!' in agendamento2.json()['detail']



def test_post_agendamento_servico_nao_cadastrado():
    cliente_teste = TestClient(criar_app(casos_de_uso()))
    resposta = cliente_teste.post('/agendamentos',json={
        'id' : '1a',
        'cliente_id' : 'c1',
        'barbeiro_id' : 'b1',
        'tipo' : 'cabelo',
        'inicio' : '2026-11-20T09:00:00'
    })

    assert resposta.status_code == 404
    assert 'Serviço não cadastrado' in resposta.json()['detail']
    

    