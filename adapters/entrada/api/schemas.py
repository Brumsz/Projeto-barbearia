'''
Entrada

AgendamentoEntrada: id, cliente_id, barbeiro_id, tipo (cabelo ou barba), inicio (datetime).
PagamentoEntrada: valor (Decimal), data (datetime), metodo (pix ou dinheiro).
AtualizarStatusAgendamento: status com valor fixo "cancelado".
AtualizarStatusPagamento: status com valor fixo "pago".

Saída

AgendamentoSaida: id, nomes do cliente e do barbeiro (quando a porta de leitura existir), tipo, preço, horário, status e pagamento (opcional).
PagamentoSaida: valor, data, método e status.
ErroSaida: {"erro": "mensagem"}, o formato padrão de erro que combinamos.

'''

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Literal,Optional


MetodoPagamentoTexto = Literal["pix", "dinheiro"]

#ENTRADA
class AgendamentoEntrada(BaseModel):
    id:str
    cliente_id: str
    barbeiro_id: str
    tipo: Literal["cabelo", "barba"]
    inicio: datetime

class PagamentoEntrada(BaseModel):
    valor:Decimal
    data:datetime
    metodo:MetodoPagamentoTexto

class AtualizarStatusAgendamento(BaseModel):
    status:Literal["cancelado"]

class AtualizarStatusPagamento(BaseModel):
    status:Literal["pago"]


#SAIDA
class PagamentoSaida(BaseModel):
    valor:Decimal
    data:datetime
    metodo:MetodoPagamentoTexto
    status: Literal["pendente", "pago", "cancelado"]

class AgendamentoSaida(BaseModel):
    id:str
    cliente_id: str
    barbeiro_id: str
    tipo: Literal["cabelo", "barba"]
    preco:Decimal
    horario: datetime
    status:Literal["ativo","cancelado"]
    pagamento:Optional[PagamentoSaida] = None



