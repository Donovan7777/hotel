# modele/reservation.py
# -----------------------------------------------------------------------------
# Fichier: modele/reservation.py
# Rôle : Modèle ORM pour "reservation".
# Notes:
#   - prix_jour en MONEY côté MSSQL, je le mappe à float côté Python.
#   - date_debut/fin en DateTime(timezone=False) donc je « naïve » les dt en entrée.
#   - FK vers usager et chambre sont NOT NULL (réservation doit référencer les deux).
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import MONEY
from uuid import UUID, uuid4
from .base import Base

if TYPE_CHECKING:
    from .usager import Usager
    from .chambre import Chambre

class Reservation(Base):
    __tablename__ = "reservation"

    id_reservation: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    date_debut_reservation: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    date_fin_reservation: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    prix_jour: Mapped[float] = mapped_column(MONEY, nullable=False)
    info_reservation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    fk_id_usager: Mapped[UUID] = mapped_column(ForeignKey("usager.id_usager"), nullable=False)
    fk_id_chambre: Mapped[UUID] = mapped_column(ForeignKey("chambre.id_chambre"), nullable=False)

    # Relations vers les entités liées (back_populates pour naviguer retour).
    usager: Mapped["Usager"] = relationship("Usager", back_populates="reservations")
    chambre: Mapped["Chambre"] = relationship("Chambre", back_populates="reservations")
