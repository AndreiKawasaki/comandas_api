# Autor: Andrei Ryuichi Kawasaki

from pydantic import BaseModel


class Produto(BaseModel):
    """Autor: Andrei Ryuichi Kawasaki"""

    id_produto: int | None = None
    nome: str
    descricao: str | None = None
    preco: float
    estoque: int

