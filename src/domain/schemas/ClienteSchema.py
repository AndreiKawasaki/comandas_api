from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    telefone: str


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None


class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cpf: str
    telefone: str

