from datetime import datetime
from decimal import Decimal

from application.use_cases.agendar_horario import AgendarHorario
from application.use_cases.cancelar_agendamento import CancelarAgendamento
from application.use_cases.confirmar_pagamento import ConfirmarPagamento
from application.use_cases.registrar_pagamento import RegistrarPagamento
from domain.servico import Servico,TipoDeServico
from domain.pagamento import Pagamento,MetodoPagamento


class CLI:
    ''' 
    Esse vai ser um CLI simples para o terminal
    '''
    def __init__(self,agendar:AgendarHorario, cancelar:CancelarAgendamento, confirmar:ConfirmarPagamento, registrar:RegistrarPagamento):
        self.agendar = agendar
        self.cancelar = cancelar
        self.confirmar = confirmar
        self.registrar = registrar

    def menu(self):
        while True:
            print("\n=== Barbearia ===")
            print("1 - Agendar horário")
            print("2 - Registrar pagamento")
            print("3 - Confirmar pagamento")
            print("4 - Cancelar agendamento")
            print("0 - Sair")
            opcao = int(input("Escolha uma opção: ").strip())

            if opcao == 0:
                break
            try:
                self._executar(opcao)
            except ValueError as e:
                print(f"Erro: {e}")
        

    def _executar(self,opcao):
        #Recebe a opcao escolhida no cli, pede os atributos que o use case precisa e o executa
        if opcao == 1:
            id_ag = input("ID do agendamento: ")
            id_cliente = input("ID do cliente: ")
            id_barbeiro = input("ID do barbeiro: ")
            servico = self._pedir_servico()
            data_texto = input("Data e hora (dd/mm/aaaa hh:mm): ")
            inicio = datetime.strptime(data_texto, "%d/%m/%Y %H:%M")

            self.agendar.executar(id_ag, id_cliente, id_barbeiro, servico, inicio)
            print("Agendado com sucesso!")

        elif opcao == 2:
            id_ag = input("ID do agendamento: ")
            pagamento = self._criar_pagamento()

            self.registrar.executar(id_ag, pagamento)
            print('Pagamento Registrado')

        elif opcao == 3:
            id_ag = input("ID do agendamento: ")

            self.confirmar.executar(id_ag)
            print('Pagamento confirmado com sucesso')

        elif opcao == 4:
            id_ag = input("ID do agendamento: ")

            self.cancelar.executar(id_ag)
            print('Agendamento cancelado')

        else:
            raise ValueError('Insira uma opção valida')
        

    def _pedir_servico(self):
        #pede para o usuario escolher entre um dos serviços e devolve o objeto
        print("1 - Corte")
        print("2 - Barba")
        escolha = input("Escolha o serviço: ").strip()

        tipos = {"1": TipoDeServico.CABELO, "2": TipoDeServico.BARBA}
        tipo = tipos.get(escolha)
        if tipo is None:
            raise ValueError("Serviço inválido")

        preco = Decimal(input("Preço do serviço: ").strip())
        return Servico(tipo, preco)



    def _criar_pagamento(self):
        #pede para o usuario os atributos necessarios para criar o pagamento e devolve o objeto
        valor = Decimal(input("Digite o valor do pagamento: ").strip())
        data_texto = input("Data e hora (dd/mm/aaaa hh:mm): ")
        data_pagamento = datetime.strptime(data_texto, "%d/%m/%Y %H:%M")
        print("1 - Dinheiro")
        print("2 - Pix")
        metodo_de_pagamento =input('Escolha um desses metodos de pagamento: ').strip()

        metodos = {'1':MetodoPagamento.DINHEIRO, '2':MetodoPagamento.PIX}
        metodo = metodos.get(metodo_de_pagamento)
        if metodo is None:
            raise ValueError('Método invalido')

        return Pagamento(valor, data_pagamento, metodo_de_pagamento)