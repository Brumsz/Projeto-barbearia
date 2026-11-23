from datetime import datetime

from application.portas import RepositorioAgendamentos
from domain.agendamento import Agendamento,StatusAgendamento
from domain.horario import Horario
from domain.servico import Servico, TipoDeServico
from application.portas import Relogio,RepositorioServicos
from application.errors.erros import HorarioIndisponivel, NaoEncontrado


class AgendarHorario:
    def __init__(self,repositorio:RepositorioAgendamentos,relogio:Relogio, repositorio_servicos: RepositorioServicos):
        self.repositorio = repositorio
        self.relogio = relogio
        self.repositorio_servicos = repositorio_servicos

    def executar(self,id:str, cliente_id:str, barbeiro_id:str, tipo:TipoDeServico, inicio:datetime):

        servico = self.repositorio_servicos.obter_por_tipo(tipo)
        if servico is None:
            raise NaoEncontrado("Serviço não cadastrado")

        horario= Horario(inicio)

        if inicio < self.relogio.agora():
            raise ValueError("Não é possível agendar no passado")

        if self.repositorio.horario_ocupado(barbeiro_id, horario ):
            raise HorarioIndisponivel('Horário Indisponivel!')

        agendamento = Agendamento(id, cliente_id, barbeiro_id, servico, horario)
        
        self.repositorio.salvar(agendamento)
        return agendamento

    