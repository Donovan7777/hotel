# modele/chambre.py
# -----------------------------------------------------------------------------
# Fichier: modele/chambre.py
# Rôle : Modèle ORM pour la table "chambre".
# Champs notables:
#   - fk_type_chambre peut être NULL (chambre orpheline permise, selon consigne).
#   - relation type_chambre (N:1) et reservations (1:N).
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, SmallInteger, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

if TYPE_CHECKING:
    from .type_chambre import TypeChambre
    from .reservation import Reservation

class Chambre(Base):
    __tablename__ = "chambre"

    id_chambre: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    numero_chambre: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    disponible_reservation: Mapped[bool] = mapped_column(Boolean, nullable=False)
    autre_informations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fk_type_chambre: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("type_chambre.id_type_chambre"), nullable=True
    )

    # back_populates permet d’aller dans les deux sens (TypeChambre.chambres)
    type_chambre: Mapped[Optional["TypeChambre"]] = relationship("TypeChambre", back_populates="chambres")
    # Une chambre peut avoir plusieurs réservations dans le temps.
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="chambre")
