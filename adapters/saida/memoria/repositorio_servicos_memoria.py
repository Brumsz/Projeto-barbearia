from domain.servico import Servico, TipoDeServico



class RepositorioServicosEmMemoria:
    def __init__(self, servicos: list[Servico]):
        self._servicos = {s.servico: s for s in servicos}

    def obter_por_tipo(self, tipo: TipoDeServico) -> Servico | None:
        return self._servicos.get(tipo)
    