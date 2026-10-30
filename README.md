# ✂️ Projeto Barbearia

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Arquitetura](https://img.shields.io/badge/Arquitetura-Hexagonal-informational)

Sistema de linha de comando para gerenciar a agenda de uma barbearia: agendamento de horários, registro e confirmação de pagamentos e cancelamento de cortes. O projeto foi construído com **arquitetura hexagonal**, separando regras de negócio, casos de uso e infraestrutura.

## ✨ Funcionalidades

- Agendamento de horários para **Corte** ou **Barba**
- Horários em hora cheia ou meia hora
- Bloqueio de horários já ocupados por outro agendamento
- Registro de pagamento (**Pix** ou **Dinheiro**), com valor igual ao preço do serviço
- Confirmação de pagamento
- Cancelamento de agendamentos (não é permitido cancelar um agendamento já pago)
- Testes unitários cobrindo as regras de negócio

## 🛠️ Tecnologias

- Python · Pytest · Dataclasses · Enum

## 📁 Estrutura do projeto

```
Projeto-barbearia/
├── domain/          # Regras de negócio puras (Agendamento, Pagamento, Servico, Horario)
├── application/     # Casos de uso (agendar, registrar/confirmar pagamento, cancelar) e portas
├── adapters/
│   ├── entrada/     # CLI: interface com o usuário pelo terminal
│   └── saida/       # Repositório em memória e relógio do sistema
├── tests/           # Testes unitários com pytest
└── main.py          # Ponto de entrada da aplicação
```

## 📐 Regras de negócio

- Um horário só pode ser agendado no futuro
- Cada barbeiro tem uma agenda: dois agendamentos ativos não podem ocupar o mesmo horário
- O valor do pagamento deve ser igual ao preço do serviço
- Um agendamento cancelado não pode receber pagamento
- Um pagamento só pode ser registrado uma vez por agendamento

## 🚀 Como instalar e rodar

**1. Clone o repositório**
```bash
git clone https://github.com/Brumsz/Projeto-barbearia.git
cd Projeto-barbearia
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a aplicação**
```bash
python main.py
```

No menu, escolha a opção desejada. Exemplo de fluxo: agendar um horário, registrar o pagamento com o mesmo valor do serviço e depois confirmar o pagamento.

> ℹ️ Os dados ficam em memória: ao encerrar o programa, os agendamentos são perdidos.

## 🧪 Rodando os testes

```bash
pytest
```

---

Desenvolvido por [João](https://github.com/Brumsz)
