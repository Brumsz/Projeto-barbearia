from domain.agendamento import Agendamento, StatusAgendamento
from domain.servico import Servico, TipoDeServico
from domain.horario import Horario
from domain.pagamento import Pagamento, MetodoPagamento, StatusPagamento



class RepositorioAgendamentoPostgres:
    def __init__(self,conexao_factory):
        self._conectar = conexao_factory

    #Funções de escrita

    def salvar(self, agendamento: Agendamento) -> None:
        with self._conectar() as conn:
            servico_id = self._servico_id(conn, agendamento.servico.servico)
            conn.execute(
                "INSERT INTO agendamentos "
                "(id, id_cliente, id_barbeiro, id_servico, preco, inicio, status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    agendamento.id,
                    agendamento.cliente_id,
                    agendamento.barbeiro_id,
                    servico_id,
                    agendamento.servico.preco,
                    agendamento.horario.inicio,
                    agendamento.status.value,
                ),
            )
            if agendamento.pagamento is not None:
                self._inserir_pagamento(conn, agendamento)


    def atualizar(self, agendamento: Agendamento) -> None:
        with self._conectar() as conn:
            conn.execute(
                "UPDATE agendamentos SET status = %s WHERE id = %s",
                (agendamento.status.value, agendamento.id),
            )
            if agendamento.pagamento is not None:
                self._salvar_ou_atualizar_pagamento(conn, agendamento)

    #Funções de Leitura
 
    def buscar(self, agendamento_id: str) -> Agendamento | None:
        with self._conectar() as conn:
            linha = conn.execute(
                "SELECT a.id, a.id_cliente, a.id_barbeiro, s.tipo, a.preco, "
                "       a.inicio, a.status "
                "FROM agendamentos a "
                "JOIN servicos s ON s.id = a.id_servico "
                "WHERE a.id = %s",
                (agendamento_id,),
            ).fetchone()
            if linha is None:
                return None

            pagamento = self._buscar_pagamento(conn, agendamento_id)

        id_, cliente_id, barbeiro_id, tipo, preco, inicio, status = linha
        return Agendamento(
            id=id_,
            cliente_id=cliente_id,
            barbeiro_id=barbeiro_id,
            servico=Servico(TipoDeServico(tipo), preco),
            horario=Horario(inicio),
            status=StatusAgendamento(status),
            pagamento=pagamento,
        )

    def horario_ocupado(self, barbeiro_id: str, horario: Horario) -> bool:
        with self._conectar() as conn:
            linha = conn.execute(
                "SELECT 1 FROM agendamentos "
                "WHERE id_barbeiro = %s AND inicio = %s AND status = %s",
                (barbeiro_id, horario.inicio, StatusAgendamento.ATIVO.value),
            ).fetchone()
        return linha is not None

    #Funções auxiliares

    def _servico_id(self, conn , servico:TipoDeServico) -> str:
            cur = conn.execute(
                'SELECT id FROM servicos WHERE tipo = %s',
                (servico.value,),
            )
    
            linha = cur.fetchone()
            if linha is None:
                raise ValueError(f"Serviço '{servico.value}' não cadastrado")
            return linha[0]
    
    
    def _inserir_pagamento(self, conn ,agendamento: Agendamento) ->  None:
        pagamento = agendamento.pagamento
        conn.execute(
            "INSERT INTO pagamentos (id_agendamento, valor, data, metodo, status)"
            "VALUES (%s, %s, %s, %s, %s)",
            (agendamento.id, pagamento.valor, pagamento.data, pagamento.metodo_de_pagamento.value, pagamento.status.value)
            )

    def _salvar_ou_atualizar_pagamento(self, conn, agendamento: Agendamento) -> None:
        p = agendamento.pagamento
        conn.execute(
            "INSERT INTO pagamentos (id_agendamento, valor, data, metodo, status) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (id_agendamento) DO UPDATE SET status = EXCLUDED.status",
            (agendamento.id, p.valor, p.data, p.metodo_de_pagamento.value, p.status.value),
        )

    def _buscar_pagamento(self, conn, agendamento_id: str) -> Pagamento | None:
        linha = conn.execute(
            "SELECT valor, data, metodo, status FROM pagamentos WHERE id_agendamento = %s",
            (agendamento_id,),
        ).fetchone()
        if linha is None:
            return None
        valor, data, metodo, status = linha
        return Pagamento(
            valor=valor,
            data=data,
            metodo_de_pagamento=MetodoPagamento(metodo),
            status=StatusPagamento(status),
        )