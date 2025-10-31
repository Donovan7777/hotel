# modele/type_chambre.py
# -----------------------------------------------------------------------------
# Fichier: modele/type_chambre.py
# Rôle : Modèle ORM pour "type_chambre" (ex.: Simple, Double, Suite).
# Détail important:
#   - prix_plafond est un NCHAR(10) (string), volontairement, pour coller à la BD
#     fournie. Les validations sont gérées dans la couche métier.
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import MONEY, NCHAR
from uuid import UUID, uuid4
from .base import Base

if TYPE_CHECKING:
    from .chambre import Chambre

class TypeChambre(Base):
    __tablename__ = "type_chambre"

    id_type_chambre: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    nom_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prix_plancher: Mapped[float] = mapped_column(MONEY, nullable=False)
    prix_plafond: Mapped[Optional[str]] = mapped_column(NCHAR(10), nullable=True)
    description_chambre: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # back_populates: la relation inverse (Chambre.type_chambre)
    chambres: Mapped[List["Chambre"]] = relationship("Chambre", back_populates="type_chambre")
