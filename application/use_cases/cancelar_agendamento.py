from application.portas import RepositorioAgendamentos
from domain.pagamento import StatusPagamento
from domain.agendamento import Agendamento

class CancelarAgendamento:
    def __init__(self, repositorio:RepositorioAgendamentos):
        self.repositorio = repositorio

    def executar(self, agendamento_id:str):

        agendamento_encontrado = self.repositorio.buscar(agendamento_id)

        if agendamento_encontrado is None:
            raise  ValueError('Agendamento não encontrado')

        #VOU DEIXAR ESSA FUNÇÃO TEMPORARIAMENTE, MUDAR DEPOIS
        if agendamento_encontrado.pagamento == StatusPagamento.PAGO:
            raise  ValueError('O corte ja foi pago e não pode ser cancelado!')

        agendamento_encontrado.cancelar()

        self.repositorio.atualizar(agendamento_encontrado)


        

        


    