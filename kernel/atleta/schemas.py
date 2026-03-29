from datetime import datetime
from typing import Annotated, Optional

from pydantic import Field, PositiveFloat

from kernel.categorias.schemas import CategoriaIn
from kernel.centro_treinamento.schemas import CentroTreinamentoAtleta
from kernel.contrib.schemas import BaseSchema


class Atleta(BaseSchema):
    nome: Annotated[
        str, Field(description='Nome do atleta', example='Joao', max_length=50)
    ]
    cpf: Annotated[
        str,
        Field(
            description='CPF do atleta', example='12345678900', max_length=11
        ),
    ]
    idade: Annotated[int, Field(description='Idade do atleta', example=25)]
    peso: Annotated[
        PositiveFloat, Field(description='Peso do atleta', example=75.5)
    ]
    altura: Annotated[
        PositiveFloat, Field(description='Altura do atleta', example=1.70)
    ]
    sexo: Annotated[
        str, Field(description='Sexo do atleta', example='M', max_length=1)
    ]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(description='Centro de treinamento do atleta'),
    ]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta):
    id: Annotated[int, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]


class AtletaListOut(BaseSchema):
    nome: Annotated[
        str, Field(description='Nome do atleta', example='Joao', max_length=50)
    ]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(description='Centro de treinamento do atleta'),
    ]


class AtletaUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(
            None, description='Nome do atleta', example='Joao', max_length=50
        ),
    ]
    idade: Annotated[
        Optional[int], Field(None, description='Idade do atleta', example=25)
    ]
