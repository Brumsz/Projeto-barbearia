from fastapi import APIRouter,HTTPException

from application.portas import RepositorioAgendamentos,RepositorioServicos
from adapters.entrada.api.schemas import AgendamentoEntrada,AgendamentoSaida
from composicao import montar_caso_de_uso

router = APIRouter(prefix='/agendamentos')

@router.post('/criar', response_model=AgendamentoEntrada,status_code=201)
def criar_agendamento(repositorio:RepositorioAgendamentos , servicos:RepositorioServicos, dados:AgendamentoEntrada) -> AgendamentoSaida:
    