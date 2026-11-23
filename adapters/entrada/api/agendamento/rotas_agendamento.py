from fastapi import APIRouter, HTTPException

from adapters.entrada.api.schemas import AgendamentoEntrada, AgendamentoSaida
from domain.servico import TipoDeServico
from application.errors.erros import HorarioIndisponivel, NaoEncontrado

def criar_router(casos: dict) -> APIRouter:
    router = APIRouter(prefix="/agendamentos")

    @router.post("", status_code=201, response_model=AgendamentoSaida)
    def criar_agendamento(dados: AgendamentoEntrada):

        try:
            tipo = TipoDeServico(dados.tipo)
            agendamento = casos['agendar'].executar(dados.id, dados.cliente_id, dados.barbeiro_id, tipo, dados.inicio)
        except NaoEncontrado as e :
            raise HTTPException(status_code=404,detail=f'{e}')
        except HorarioIndisponivel as e :
            raise HTTPException(status_code=409,detail=f'{e}')
        except ValueError as e:
            raise HTTPException(status_code=400,detail=f'{e}')

        return AgendamentoSaida(id=agendamento.id, cliente_id= agendamento.cliente_id, barbeiro_id= agendamento.barbeiro_id, tipo=agendamento.servico.servico.value, preco=agendamento.servico.preco, horario= agendamento.horario.inicio, status=agendamento.status.value)
        



    return router