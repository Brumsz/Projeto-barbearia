from application.portas import RepositorioAgendamentos 

class ConfirmarPagamento:
    def __init__(self,repositorio:RepositorioAgendamentos):
        self.repositorio = repositorio

    def executar(self, agendamento_id:str) -> None:

        agendamento_encontrado = self.repositorio.buscar(agendamento_id)

        if agendamento_encontrado is None:
            raise  ValueError('Agendamento não encontrado')

        agendamento_encontrado.confirmar_pagamento()

        self.repositorio.atualizar(agendamento_encontrado)


        