from domain.servico import Servico, TipoDeServico


class RepositorioServicosPostgres:
    def __init__(self, conexao_factory):
        self._conectar = conexao_factory

    def obter_por_tipo(self, tipo: TipoDeServico) -> Servico | None:
        with self._conectar() as conn:
            linha = conn.execute(
                "SELECT preco FROM servicos WHERE tipo = %s",
                (tipo.value,),
            ).fetchone()

        if linha is None:
            return None
        return Servico(tipo, linha[0])

