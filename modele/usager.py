# modele/usager.py
# -----------------------------------------------------------------------------
# Fichier: modele/usager.py
# Rôle : Modèle ORM pour "usager".
# Notes:
#   - mobile et mot_de_passe en CHAR avec longueur fixe (comme la BD).
#   - relation 1:N vers Reservation.
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.dialects.mssql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base

if TYPE_CHECKING:
    from .reservation import Reservation

class Usager(Base):
    __tablename__ = "usager"

    id_usager: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    adresse: Mapped[str] = mapped_column(String(100), nullable=False)
    mobile: Mapped[str] = mapped_column(CHAR(15), nullable=False)
    mot_de_passe: Mapped[str] = mapped_column(CHAR(60), nullable=False)
    type_usager: Mapped[str] = mapped_column(String(50), nullable=False)

    # Un usager peut avoir plusieurs réservations.
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="usager")
