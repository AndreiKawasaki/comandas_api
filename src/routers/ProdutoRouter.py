# Autor: Andrei Ryuichi Kawasaki

from fastapi import APIRouter

from domain.entities.Produto import Produto


router = APIRouter()


@router.get("/produto/", tags=["Produto"], status_code=200)
def get_produtos():
    return {"msg": "produto get todos executado"}


@router.get("/produto/{id}", tags=["Produto"], status_code=200)
def get_produto(id: int):
    return {"msg": "produto get um executado", "id": id}


@router.post("/produto/", tags=["Produto"], status_code=200)
def post_produto(corpo: Produto):
    return {
        "msg": "produto post executado",
        "nome": corpo.nome,
        "descricao": corpo.descricao,
        "preco": corpo.preco,
        "estoque": corpo.estoque,
    }


@router.put("/produto/{id}", tags=["Produto"], status_code=200)
def put_produto(id: int, corpo: Produto):
    return {
        "msg": "produto put executado",
        "id": id,
        "nome": corpo.nome,
        "descricao": corpo.descricao,
        "preco": corpo.preco,
        "estoque": corpo.estoque,
    }


@router.delete("/produto/{id}", tags=["Produto"], status_code=200)
def delete_produto(id: int):
    return {"msg": "produto delete executado", "id": id}

