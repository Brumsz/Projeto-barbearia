from fastapi import FastAPI
from adapters.entrada.api.agendamento.rotas_agendamento import criar_router

def criar_app(casos: dict) -> FastAPI:
    app = FastAPI()
    app.include_router(criar_router(casos))
    
    return app