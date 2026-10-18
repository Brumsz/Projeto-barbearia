from datetime import datetime
from decimal import Decimal

import pytest

from domain.cliente import Cliente
from domain.barbeiro import Barbeiro
from domain.servico import Servico,TipoDeServico
from domain.horario import Horario
from domain.pagamento import Pagamento, MetodoPagamento
from domain.agendamento import Agendamento

def test_cria_todos_os_dominios():
    cliente = Cliente("c1", "João")
    barbeiro = Barbeiro("b1", "Kaique")
    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    horario = Horario(datetime(2026, 10, 20, 9, 0))
    pagamento = Pagamento(Decimal("30.00"), datetime(2026, 10, 20, 9, 0), MetodoPagamento.PIX)
    agendamento = Agendamento("a1", cliente.id, barbeiro.id, servico, horario)

    assert agendamento.pagamento is None

def test_horario_rejeita_minutos_quebrados():
    with pytest.raises(ValueError):
        Horario(datetime(2026, 10, 20, 9, 15))


def test_agendamento_exige_cliente_e_barbeiro():
    servico = Servico(TipoDeServico.CABELO, Decimal("30.00"))
    horario = Horario(datetime(2026, 10, 20, 9, 0))
    with pytest.raises(ValueError):
        Agendamento("a1", "", "b1", servico, horario)