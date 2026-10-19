from application.portas import RepositorioAgendamentos 
from domain.pagamento import Pagamento

class RegistrarPagamento:
    def __init__(self,repositorio:RepositorioAgendamentos):
        self.repositorio = repositorio

    def executar(self, agendamento_id:str, pagamento:Pagamento):

        agendamento_encontrado = self.repositorio.buscar(agendamento_id)

        if agendamento_encontrado is None:
            raise  ValueError('Agendamento não encontrado')

        agendamento_encontrado.registrar_pagamento(pagamento)

        self.repositorio.atualizar(agendamento_encontrado)        