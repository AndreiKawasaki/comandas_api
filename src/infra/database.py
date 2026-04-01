from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

from settings import STR_DATABASE

# cria o engine do banco de dados
engine = create_engine(STR_DATABASE, echo=True)

# cria a sessão do banco de dados
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)

# para trabalhar com tabelas
Base = declarative_base()


def _seed_admin_if_missing():
    """Insere funcionário admin (CPF 1 / senha abcBolinhas) se não existir — alinhado ao roteiro da aula."""
    from infra.orm.FuncionarioModel import FuncionarioDB
    from infra.security import get_password_hash

    db = SessionLocal()
    try:
        if db.query(FuncionarioDB).filter(FuncionarioDB.cpf == "1").first() is not None:
            return
        admin = FuncionarioDB(
            id=None,
            nome="Admin",
            matricula="1",
            cpf="1",
            telefone="1",
            grupo=1,
            senha=get_password_hash("abcBolinhas"),
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()


# cria, caso não existam, as tabelas de todos os modelos que encontrar na aplicação (importados)
async def cria_tabelas():
    from infra.orm import (  # noqa: F401
        ClienteModel,
        FuncionarioModel,
        ProdutoModel,
        ComandaModel,
        CaixaModel,
    )

    Base.metadata.create_all(engine)
    _seed_admin_if_missing()


# dependência para injetar a sessão do banco de dados nas rotas
def get_db():
    db_session: SQLAlchemySession = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

