# Autor: Andrei Ryuichi Kawasaki

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Domain Schemas
from domain.schemas.FuncionarioSchema import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioResponse,
)

# Infra
from infra.orm.FuncionarioModel import FuncionarioDB
from infra.database import get_db

router = APIRouter()

@router.get(
    "/funcionario/",
    response_model=List[FuncionarioResponse],
    tags=["Funcionário"],
    status_code=status.HTTP_200_OK,
)
async def get_funcionarios(db: Session = Depends(get_db)):
    try:
        funcionarios = db.query(FuncionarioDB).all()
        return funcionarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar funcionários: {str(e)}",
        )

@router.get(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    tags=["Funcionário"],
    status_code=status.HTTP_200_OK,
)
async def get_funcionario(id: int, db: Session = Depends(get_db)):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado",
            )
        return funcionario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar funcionário: {str(e)}",
        )

@router.post(
    "/funcionario/",
    response_model=FuncionarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Funcionário"],
)
async def post_funcionario(
    funcionario_data: FuncionarioCreate, db: Session = Depends(get_db)
):
    try:
        existing = (
            db.query(FuncionarioDB)
            .filter(FuncionarioDB.cpf == funcionario_data.cpf)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um funcionário com este CPF",
            )

        novo = FuncionarioDB(
            id=None,
            nome=funcionario_data.nome,
            matricula=funcionario_data.matricula,
            cpf=funcionario_data.cpf,
            telefone=funcionario_data.telefone,
            grupo=funcionario_data.grupo,
            senha=funcionario_data.senha,
        )
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar funcionário: {str(e)}",
        )

@router.put(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    tags=["Funcionário"],
    status_code=status.HTTP_200_OK,
)
async def put_funcionario(
    id: int, funcionario_data: FuncionarioUpdate, db: Session = Depends(get_db)
):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado",
            )

        if funcionario_data.cpf and funcionario_data.cpf != funcionario.cpf:
            existing = (
                db.query(FuncionarioDB)
                .filter(FuncionarioDB.cpf == funcionario_data.cpf)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe um funcionário com este CPF",
                )

        update_data = funcionario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(funcionario, field, value)

        db.commit()
        db.refresh(funcionario)
        return funcionario
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar funcionário: {str(e)}",
        )


@router.delete(
    "/funcionario/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Funcionário"],
    summary="Remover funcionário",
)
async def delete_funcionario(id: int, db: Session = Depends(get_db)):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado",
            )
        db.delete(funcionario)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar funcionário: {str(e)}",
        )