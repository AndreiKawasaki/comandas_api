from infra import database
from sqlalchemy import Column, DateTime, Float, Integer, VARCHAR
from sqlalchemy.sql import func


class CaixaDB(database.Base):
    __tablename__ = "tb_caixa"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    status = Column(VARCHAR(20), nullable=False, index=True, default="aberto")
    data_abertura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    saldo_inicial = Column(Float, nullable=False, default=0.0)
    saldo_final = Column(Float, nullable=True)

    def __init__(self, id, status, data_abertura, data_fechamento, saldo_inicial, saldo_final):
        self.id = id
        self.status = status
        self.data_abertura = data_abertura
        self.data_fechamento = data_fechamento
        self.saldo_inicial = saldo_inicial
        self.saldo_final = saldo_final
