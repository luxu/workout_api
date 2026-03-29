from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from kernel.atleta.models import AtletaModel
from kernel.atleta.schemas import (
    AtletaIn,
    AtletaListOut,
    AtletaOut,
    AtletaUpdate,
)
from kernel.categorias.models import CategoriaModel
from kernel.centro_treinamento.models import CentroTreinamentoModel
from kernel.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.',
        )

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(
                    nome=centro_treinamento_nome
                )
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento '
            f'{centro_treinamento_nome} não foi encontrado.',
        )
    try:
        atleta_model = AtletaModel(
            created_at=datetime.utcnow(),
            **atleta_in.model_dump(
                exclude={'categoria', 'centro_treinamento'}
            ),
        )
        atleta_model.categoria_id = categoria.id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        atleta_model.categoria = categoria
        atleta_model.centro_treinamento = centro_treinamento

        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                'Já existe um atleta cadastrado com o cpf: '
                f'{atleta_in.cpf}'
            ),
        )
    except Exception as err:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f'Ocorreu um erro ao inserir os dados no banco\n{err}'
            ),
        )

    return AtletaOut.model_validate(atleta_model)


@router.get(
    '/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    # response_model=LimitOffsetPage[AtletaListOut],
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:

    atletas: list[AtletaOut] = (
        await db_session.execute(select(AtletaModel))
    ).scalars().all()

    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: int, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        (
            await db_session.execute(
                select(AtletaModel)
                .options(
                    selectinload(AtletaModel.categoria),
                    selectinload(AtletaModel.centro_treinamento),
                )
                .filter_by(id=id)
            )
        )
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    return atleta


@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: int,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
) -> AtletaOut:
    atleta: AtletaOut = (
        (
            await db_session.execute(
                select(AtletaModel)
                .options(
                    selectinload(AtletaModel.categoria),
                    selectinload(AtletaModel.centro_treinamento),
                )
                .filter_by(id=id)
            )
        )
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: int, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}',
        )

    await db_session.delete(atleta)
    await db_session.commit()
