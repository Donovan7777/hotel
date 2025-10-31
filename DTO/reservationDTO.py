# DTO/reservationDTO.py
# -----------------------------------------------------------------------------
# Fichier: DTO/reservationDTO.py
# Rôle : DTOs pour réservations, incluant:
#   - CriteresRechercheDTO (alias legacy demandé)
#   - ReservationDTO (réponse complète)
#   - ReservationCreateDTO (payload minimal pour POST /reservations)
#   - ReservationUpdateDTO (patch partiel)
# Détails:
#   - Validations de base: dateFin > dateDebut (dans deux DTOs).
#   - Constructeur from_entity pour convertir l’ORM -> DTO propre.
# -----------------------------------------------------------------------------

from __future__ import annotations

import datetime
from typing import Optional, overload
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict

from modele.reservation import Reservation as ReservationEntity
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO

# -------------------- Recherche (legacy alias demandé) --------------------
# DTO souple pour anciennes recherches. y’a une règle: nom et prénom doivent
# être fournis ensemble (sinon erreur). Ça évite des queries weird.
class CriteresRechercheDTO(BaseModel):
    idReservation: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idChambre: Optional[str] = Field(default=None, min_length=36, max_length=36)
    nom: Optional[str] = Field(default=None, max_length=60)
    prenom: Optional[str] = Field(default=None, max_length=60)

    def model_post_init(self, __ctx) -> None:
        if (self.nom and not self.prenom) or (self.prenom and not self.nom):
            raise ValueError("Le nom et le prénom doivent être tous les deux présents ou absents.")

RechercherReservationDTO = CriteresRechercheDTO  # alias exigé

# -------------------- DTO principal (réponse complète) --------------------
# C’est le DTO complet qui sort des GET/POST/PUT.
class ReservationDTO(BaseModel):
    idReservation: Optional[UUID] = None
    dateDebut: datetime.datetime
    dateFin: datetime.datetime
    prixParJour: float
    infoReservation: Optional[str] = None
    chambre: ChambreDTO
    usager: UsagerDTO

    # Validation: fin après début (classique).
    @field_validator("dateFin")
    @classmethod
    def _end_after_start(cls, fin, info):
        debut = info.data.get("dateDebut")
        if debut and fin and fin <= debut:
            raise ValueError("La date de fin doit être après la date de début.")
        return fin

    # constructeur à partir de l'entité modèle
    # Surcharge: soit on passe ReservationEntity directement, soit kwargs.
    @overload
    def __init__(self, r: ReservationEntity): ...
    @overload
    def __init__(self, **data): ...
    def __init__(self, *args, **kwargs):
        if args and len(args) == 1 and not kwargs:
            r = args[0]
            # Je mappe chaque champ du modèle vers le DTO. Note: prix_jour -> float.
            super().__init__(
                idReservation=getattr(r, "id_reservation"),
                dateDebut=getattr(r, "date_debut_reservation"),
                dateFin=getattr(r, "date_fin_reservation"),
                prixParJour=float(getattr(r, "prix_jour")),
                infoReservation=getattr(r, "info_reservation"),
                chambre=ChambreDTO(getattr(r, "chambre")),
                usager=UsagerDTO(getattr(r, "usager")),
            )
        else:
            super().__init__(**kwargs)

    @classmethod
    def from_entity(cls, r: ReservationEntity) -> "ReservationDTO":
        # Petite helper pour que l’appelant fasse ReservationDTO.from_entity(r) direct.
        return cls(r)

# -------------------- DTO de création minimal (IDs seulement) -------------
# Sert au POST /reservations avec un body simple à produire côté front.
class ReservationCreateDTO(BaseModel):
    """
    Payload minimal pour créer une réservation:
    - idUsager (UUID)
    - idChambre (UUID)
    - dateDebut (datetime)
    - dateFin (datetime)
    - prixParJour (float)
    - infoReservation (str | None)
    """
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "idUsager": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "idChambre": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "dateDebut": "2025-11-01T15:00:00",
            "dateFin":   "2025-11-03T11:00:00",
            "prixParJour": 129.99,
            "infoReservation": "Demande étage élevé"
        }
    })

    idUsager: UUID
    idChambre: UUID
    dateDebut: datetime.datetime
    dateFin: datetime.datetime
    prixParJour: float
    infoReservation: Optional[str] = None

    # Revalide date fin après date début (mieux trop que pas assez).
    @field_validator("dateFin")
    @classmethod
    def _end_after_start(cls, fin, info):
        debut = info.data.get("dateDebut")
        if debut and fin and fin <= debut:
            raise ValueError("La date de fin doit être après la date de début.")
        return fin

# -------------------- DTO de mise à jour partielle ------------------------
# Patch de réservation: tout est optionnel, on laisse ce qui est None intact.
class ReservationUpdateDTO(BaseModel):
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idChambre: Optional[str] = Field(default=None, min_length=36, max_length=36)
    dateDebut: Optional[datetime.datetime] = None
    dateFin: Optional[datetime.datetime] = None
    prixParJour: Optional[float] = None
    infoReservation: Optional[str] = None

    def model_post_init(self, __ctx) -> None:
        if self.dateDebut and self.dateFin and self.dateFin <= self.dateDebut:
            raise ValueError("La date de fin doit être après la date de début.")
