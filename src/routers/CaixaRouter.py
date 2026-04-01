# Autor: Andrei Ryuichi Kawasaki

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.CaixaSchema import CaixaCreate, CaixaUpdate, CaixaResponse
from infra.database import get_db
from infra.dependencies import require_group
from infra.orm.CaixaModel import CaixaDB

router = APIRouter()


@router.get(
    "/caixa/",
    response_model=List[CaixaResponse],
    tags=["Caixa"],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os caixas (grupos 1 e 3)",
)
async def get_caixas(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
):
    try:
        return db.query(CaixaDB).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar caixas: {str(e)}",
        )


@router.get(
    "/caixa/{id}",
    response_model=CaixaResponse,
    tags=["Caixa"],
    status_code=status.HTTP_200_OK,
    summary="Buscar caixa por ID (grupos 1 e 3)",
)
async def get_caixa(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
):
    try:
        caixa = db.query(CaixaDB).filter(CaixaDB.id == id).first()
        if not caixa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caixa não encontrado",
            )
        return caixa
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar caixa: {str(e)}",
        )


@router.post(
    "/caixa/",
    response_model=CaixaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Caixa"],
    summary="Criar novo caixa (grupos 1 e 3)",
)
async def post_caixa(
    caixa_data: CaixaCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3])),
):
    try:
        novo = CaixaDB(
            id=None,
            status="aberto",
            data_abertura=None,
            data_fechamento=None,
            saldo_inicial=caixa_data.saldo_inicial,
            saldo_final=None,
        )
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar caixa: {str(e)}",
        )


@router.put(
    "/caixa/{id}",
    response_model=CaixaResponse,
    tags=["Caixa"],
    status_code=status.HTTP_200_OK,
    summary="Atualizar caixa (grupo 1)",
)
async def put_caixa(
    id: int,
    caixa_data: CaixaUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
):
    try:
        caixa = db.query(CaixaDB).filter(CaixaDB.id == id).first()
        if not caixa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caixa não encontrado",
            )
        update_data = caixa_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(caixa, field, value)
        db.commit()
        db.refresh(caixa)
        return caixa
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar caixa: {str(e)}",
        )


@router.delete(
    "/caixa/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Caixa"],
    summary="Remover caixa (grupo 1)",
)
async def delete_caixa(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
):
    try:
        caixa = db.query(CaixaDB).filter(CaixaDB.id == id).first()
        if not caixa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caixa não encontrado",
            )
        db.delete(caixa)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar caixa: {str(e)}",
        )

