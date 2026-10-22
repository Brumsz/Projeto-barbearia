from datetime import datetime
from decimal import Decimal

from adapters.saida.repositorio_memoria import RepositorioAgendamentoEmMemoria
from adapters.saida.relogio_sistema import RelogioSistema
from application.use_cases.confirmar_pagamento import ConfirmarPagamento
from application.use_cases.agendar_horario import AgendarHorario
from application.use_cases.registrar_pagamento import RegistrarPagamento
from application.use_cases.cancelar_agendamento import CancelarAgendamento
from domain.agendamento import StatusPagamento,Agendamento
from domain.servico import Servico,TipoDeServico
from domain.pagamento import Pagamento,MetodoPagamento
from adapters.entrada.cli import CLI


def main():
    repositorio = RepositorioAgendamentoEmMemoria()
    relogio = RelogioSistema()
    CLI(AgendarHorario(repositorio, relogio), CancelarAgendamento(repositorio), ConfirmarPagamento(repositorio), RegistrarPagamento(repositorio)).menu()

if __name__ == '__main__':
    main()






