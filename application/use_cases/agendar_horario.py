from datetime import datetime

from application.portas import RepositorioAgendamentos
from domain.agendamento import Agendamento,StatusAgendamento
from domain.horario import Horario
from domain.servico import Servico
from application.portas import Relogio


class AgendarHorario:
    def __init__(self,repositorio:RepositorioAgendamentos,relogio:Relogio):
        self.repositorio = repositorio
        self.relogio = relogio

    def executar(self,id:str, cliente_id:str, barbeiro_id:str, servico: Servico,inicio:datetime):

        horario= Horario(inicio)

        if inicio < self.relogio.agora():
            raise ValueError("Não é possível agendar no passado")

        if self.repositorio.horario_ocupado(barbeiro_id, horario ):
            raise ValueError('Hórario Indisponível!')

        agendamento = Agendamento(id, cliente_id, barbeiro_id, servico, horario)
        
        self.repositorio.salvar(agendamento)
        return agendamento

    