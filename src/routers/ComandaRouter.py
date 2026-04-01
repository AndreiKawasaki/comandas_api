# Autor: Andrei Ryuichi Kawasaki

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.AuthSchema import FuncionarioAuth
from domain.schemas.ComandaSchema import (
    ComandaCreate,
    ComandaUpdate,
    ComandaResponse,
    FecharAbertasResponse,
)
from infra.database import get_db
from infra.dependencies import get_current_active_user, require_group
from infra.orm.ComandaModel import ComandaDB

router = APIRouter()


@router.get(
    "/comanda/",
    response_model=List[ComandaResponse],
    tags=["Comanda"],
    status_code=status.HTTP_200_OK,
    summary="Listar todas as comandas (protegida)",
)
async def get_comandas(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
):
    try:
        return db.query(ComandaDB).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar comandas: {str(e)}",
        )


@router.get(
    "/comanda/{id}",
    response_model=ComandaResponse,
    tags=["Comanda"],
    status_code=status.HTTP_200_OK,
    summary="Buscar comanda por ID (protegida)",
)
async def get_comanda(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
):
    try:
        comanda = db.query(ComandaDB).filter(ComandaDB.id == id).first()
        if not comanda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comanda não encontrada",
            )
        return comanda
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar comanda: {str(e)}",
        )


@router.post(
    "/comanda/",
    response_model=ComandaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Comanda"],
    summary="Criar nova comanda (protegida)",
)
async def post_comanda(
    comanda_data: ComandaCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user),
):
    try:
        novo = ComandaDB(
            id=None,
            status="aberta",
            data_abertura=None,
            data_fechamento=None,
            valor_total=comanda_data.valor_total,
        )
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar comanda: {str(e)}",
        )


@router.put(
    "/comanda/{id}",
    response_model=ComandaResponse,
    tags=["Comanda"],
    status_code=status.HTTP_200_OK,
    summary="Atualizar comanda (grupo 1)",
)
async def put_comanda(
    id: int,
    comanda_data: ComandaUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
):
    try:
        comanda = db.query(ComandaDB).filter(ComandaDB.id == id).first()
        if not comanda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comanda não encontrada",
            )
        update_data = comanda_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comanda, field, value)
        db.commit()
        db.refresh(comanda)
        return comanda
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar comanda: {str(e)}",
        )


@router.delete(
    "/comanda/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Comanda"],
    summary="Remover comanda (grupo 1)",
)
async def delete_comanda(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
):
    try:
        comanda = db.query(ComandaDB).filter(ComandaDB.id == id).first()
        if not comanda:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comanda não encontrada",
            )
        db.delete(comanda)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar comanda: {str(e)}",
        )


@router.post(
    "/comanda/fechar-abertas",
    response_model=FecharAbertasResponse,
    tags=["Comanda"],
    status_code=status.HTTP_200_OK,
    summary="Fechar comandas abertas por engano (grupo 1)",
)
async def fechar_comandas_abertas(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1])),
):
    try:
        abertas = db.query(ComandaDB).filter(ComandaDB.status == "aberta").all()
        agora = datetime.now(timezone.utc)
        for c in abertas:
            c.status = "fechada"
            c.data_fechamento = agora
        db.commit()
        return FecharAbertasResponse(fechadas=len(abertas))
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao fechar comandas abertas: {str(e)}",
        )

