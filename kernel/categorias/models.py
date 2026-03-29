from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from kernel.contrib.models import table_registry


@table_registry.mapped_as_dataclass
class CategoriaModel:
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')
