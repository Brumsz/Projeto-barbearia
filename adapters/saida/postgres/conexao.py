import psycopg


def abrir_conexao(database_url: str) -> psycopg.Connection:
    return psycopg.connect(database_url)

