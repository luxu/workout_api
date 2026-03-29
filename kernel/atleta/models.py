from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kernel.categorias.models import CategoriaModel
from kernel.centro_treinamento.models import CentroTreinamentoModel
from kernel.contrib.models import table_registry


@table_registry.mapped_as_dataclass
class AtletaModel:
    __tablename__ = 'atletas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey('categorias.id'), init=False
    )
    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey('centros_treinamento.pk_id'), init=False
    )
    categoria: Mapped[CategoriaModel] = relationship(
        CategoriaModel, lazy='selectin', init=False
    )
    centro_treinamento: Mapped[CentroTreinamentoModel] = relationship(
        CentroTreinamentoModel, lazy='selectin', init=False
    )
