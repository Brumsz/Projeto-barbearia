from composicao import montar_caso_de_uso
from adapters.entrada.cli import CLI


def main():
    casos_de_uso = montar_caso_de_uso()
    CLI(**casos_de_uso).menu()

if __name__ == '__main__':
    main()






