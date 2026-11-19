from datetime import datetime
from typing import Protocol

from domain.agendamento import Agendamento
from domain.servico import Servico, TipoDeServico



class RepositorioAgendamentos(Protocol):
    def horario_ocupado(self,barbeiro_id:str, inicio:datetime) -> bool: ...
    def salvar(self, agendamento:Agendamento) -> None: ...
    def buscar(self, agendamento_id:str) -> Agendamento | None: ...
    def atualizar(self, agendamento: Agendamento) -> None: ...


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class RepositorioServicos(Protocol):
    def obter_por_tipo(self, tipo: TipoDeServico) -> Servico | None: ...