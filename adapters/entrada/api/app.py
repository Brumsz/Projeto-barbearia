from fastapi import FastAPI

def criar_app(casos: dict) -> FastAPI:
    app = FastAPI()

    return app