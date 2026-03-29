from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from kernel.categorias.models import CategoriaModel
from kernel.categorias.schemas import CategoriaIn, CategoriaOut
from kernel.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    '/',
    summary='Create uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...),
) -> CategoriaOut:
    categoria_model = CategoriaModel(**categoria_in.model_dump())

    try:
        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                'Já existe uma categoria cadastrada com o nome: '
                f'{categoria_in.nome}'
            ),
        )

    return CategoriaOut.model_validate(categoria_model)


@router.get(
    '/',
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency,
) -> LimitOffsetPage[CategoriaOut]:
    return await paginate(db_session, select(CategoriaModel))


@router.get(
    '/all', status_code=status.HTTP_200_OK, response_model=list[CategoriaOut]
)
def getall():
    list_categories = {'id': 1, 'nome': 'Scale'}
    categories: list[dict[str, int]] = list_categories
    return categories


@router.get(
    '/{id}',
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria não encontrada no id: {id}',
        )

    return categoria
