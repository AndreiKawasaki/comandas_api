# Autor: Andrei Ryuichi Kawasaki

from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

from routers import AuthRouter
from routers import FuncionarioRouter
from routers import ClienteRouter
from routers import ProdutoRouter
from routers import ComandaRouter
from routers import CaixaRouter

from infra import database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API has started")
    await database.cria_tabelas()
    yield
    print("API is shutting down")


# persistAuthorization=False evita o Swagger guardar o Bearer no navegador e “parecer” que
# a rota funciona sem login depois de um Authorize anterior.
app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": False},
)


@app.get("/", tags=["Root"], status_code=200)
async def root():
    return {
        "detail": "API Pastelaria",
        "autor": "Andrei Ryuichi Kawasaki",
        "Swagger UI": "http://127.0.0.1:8000/docs",
        "ReDoc": "http://127.0.0.1:8000/redoc",
    }


app.include_router(AuthRouter.router)
app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)
app.include_router(ComandaRouter.router)
app.include_router(CaixaRouter.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=RELOAD)
