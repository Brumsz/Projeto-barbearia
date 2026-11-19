from config import carregar_cofiguracao
from adapters.saida.postgres.conexao import abrir_conexao
from adapters.saida.postgres.repositorio_postgres import RepositorioAgendamentoPostgres
from adapters.saida.postgres.repositorio_servicos_postgres import RepositorioServicosPostgres
from application.use_cases.agendar_horario import AgendarHorario
from application.use_cases.cancelar_agendamento import CancelarAgendamento
from application.use_cases.confirmar_pagamento import ConfirmarPagamento
from application.use_cases.registrar_pagamento import RegistrarPagamento
from adapters.saida.relogio_sistema import RelogioSistema



def montar_caso_de_uso():
    config = carregar_cofiguracao()
    fabrica = lambda: abrir_conexao(config.database_url)

    repositorio = RepositorioAgendamentoPostgres(fabrica)
    repositorio_de_servicos = RepositorioServicosPostgres(fabrica)
    relogio = RelogioSistema()

    return {
        "agendar": AgendarHorario(repositorio, relogio, repositorio_de_servicos),
        "cancelar": CancelarAgendamento(repositorio),
        "confirmar": ConfirmarPagamento(repositorio),
        "registrar": RegistrarPagamento(repositorio),
    }