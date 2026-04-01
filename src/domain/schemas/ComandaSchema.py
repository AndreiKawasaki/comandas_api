from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComandaCreate(BaseModel):
    valor_total: float = 0.0


class ComandaUpdate(BaseModel):
    status: Optional[str] = None
    data_fechamento: Optional[datetime] = None
    valor_total: Optional[float] = None


class ComandaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    valor_total: float


class FecharAbertasResponse(BaseModel):
    fechadas: int
