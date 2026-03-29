from typing import Annotated

from pydantic import Field

from kernel.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[
        str,
        Field(description='Nome da categoria', example='Scale', max_length=10),
    ]


class CategoriaOut(CategoriaIn):
    id: Annotated[int, Field(description='Identificador da categoria')]
