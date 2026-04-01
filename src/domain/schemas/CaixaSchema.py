from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CaixaCreate(BaseModel):
    saldo_inicial: float = 0.0


class CaixaUpdate(BaseModel):
    status: Optional[str] = None
    data_fechamento: Optional[datetime] = None
    saldo_inicial: Optional[float] = None
    saldo_final: Optional[float] = None


class CaixaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    saldo_inicial: float
    saldo_final: Optional[float] = None
