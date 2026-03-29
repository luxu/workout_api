from uuid import UUID, uuid4

from sqlalchemy import UUID as SAUUID
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from kernel.contrib.models import table_registry


@table_registry.mapped_as_dataclass
class CentroTreinamentoModel:
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, init=False
    )
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
    id: Mapped[UUID] = mapped_column(
        SAUUID(as_uuid=True), default=uuid4, nullable=False
    )
    # atleta: Mapped['AtletaModel'] = relationship(
    #     back_populates='centro_treinamento'
    # )
