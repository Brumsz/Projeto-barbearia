
from domain.agendamento import Agendamento,StatusAgendamento

class RepositorioAgendamentoEmMemoria:
    def __init__(self):
        self.agendamentos: list[Agendamento] = []

    def horario_ocupado(self, barbeiro_id, inicio) -> bool:
        return any(
            a.barbeiro_id == barbeiro_id
            and a.horario.inicio == inicio
            and a.status == StatusAgendamento.ATIVO
            for a in self.agendamentos
        )
    
    def salvar(self, agendamento:Agendamento) -> None:
        self.agendamentos.append(agendamento)

    def buscar(self, agendamento_id:str) -> Agendamento | None:
        return next(
        (a for a in self.agendamentos if a.id == agendamento_id),
        None,
    )
    
    def atualizar(self, agendamento: Agendamento) -> None:
        for i, a in enumerate(self.agendamentos):
            if a.id == agendamento.id:
                self.agendamentos[i] = agendamento
                return

