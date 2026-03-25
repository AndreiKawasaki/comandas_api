# Autor: Andrei Ryuichi Kawasaki

from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

# import das classes com as rotas/endpoints
from routers import FuncionarioRouter
from routers import ClienteRouter
from routers import ProdutoRouter

from infra import database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API has started")
    await database.cria_tabelas()
    yield
    print("API is shutting down")


app = FastAPI(lifespan=lifespan)

# mapeamento das rotas/endpoints
app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=RELOAD)


# rota padrão
@app.get("/", tags=["Root"], status_code=200)
async def root():
    return {
        "detail": "API Pastelaria",
        "autor": "Andrei Ryuichi Kawasaki",
        "Swagger UI": "http://127.0.0.1:8000/docs",
        "ReDoc": "http://127.0.0.1:8000/redoc",
    }