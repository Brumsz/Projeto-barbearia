import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    database_url: str

def carregar_cofiguracao() -> Config:
    url = os.getenv('DATABASE_URL')
    if not url:
        raise RuntimeError("DATABASE_URL não definida. Crie o arquivo .env")
    return Config(database_url=url)

