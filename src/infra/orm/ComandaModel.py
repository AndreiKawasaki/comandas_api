from infra import database
from sqlalchemy import Column, DateTime, Float, Integer, VARCHAR
from sqlalchemy.sql import func


class ComandaDB(database.Base):
    __tablename__ = "tb_comanda"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # status simples para atender ao PDF (aberta/fechada/cancelada)
    status = Column(VARCHAR(20), nullable=False, index=True, default="aberta")
    data_abertura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    valor_total = Column(Float, nullable=False, default=0.0)

    def __init__(self, id, status, data_abertura, data_fechamento, valor_total):
        self.id = id
        self.status = status
        self.data_abertura = data_abertura
        self.data_fechamento = data_fechamento
        self.valor_total = valor_total
