# metier/reservationMetier.py
# -----------------------------------------------------------------------------
# Fichier: metier/reservationMetier.py
# Rôle : logique métier pour Réservation (CRUD, règles de base).
# Points clés:
#   - _naive(): enlève timezone des datetime (DB stocke timezone=False).
#   - Création par DTO complet (legacy) ET création minimaliste par IDs.
#   - Validations: dateFin > dateDebut, prixParJour > 0, usager/chambre existent.
#   - Update: même validation pour prix > 0; dates cohérentes.
#   - On recharge les relations après create (selectinload) pour retourner un DTO plein.
# -----------------------------------------------------------------------------

from __future__ import annotations

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from core.db import SessionLocal
from DTO.reservationDTO import (
    CriteresRechercheDTO,   # compat ancien, non exposé en route
    ReservationDTO,
    ReservationCreateDTO,
    ReservationUpdateDTO,
)
from modele.reservation import Reservation
from modele.chambre import Chambre
from modele.usager import Usager

def _naive(dt):
    """Enlève la timezone si fournie (DB en timezone=False)."""
    # Juste pour éviter d’insérer un datetime aware dans une colonne naïve.
    return dt.replace(tzinfo=None) if getattr(dt, "tzinfo", None) else dt

# ------------------------------ LIST -----------------------------
def listerReservations() -> List["ReservationDTO"]:
    # Retourne toutes les résas triées par date de début (utile pour UI).
    with SessionLocal() as s:
        rows = s.execute(
            select(Reservation).order_by(Reservation.date_debut_reservation)
        ).scalars().all()
        return [ReservationDTO.from_entity(r) for r in rows]

# --------------------------- GET par ID ---------------------------
def getReservationParId(id_reservation: str) -> Optional["ReservationDTO"]:
    # Récupère une résa précise par son UUID (ou None si existe pas).
    with SessionLocal() as s:
        r = s.get(Reservation, id_reservation)
        return ReservationDTO.from_entity(r) if r else None

# ------------------------- RECHERCHE (legacy) --------------------
def rechercherReservation(criteres: CriteresRechercheDTO) -> List["ReservationDTO"]:
    # Minimal: si pas d’idReservation, je renvoie []. Ça match la consigne.
    with SessionLocal() as s:
        if not criteres.idReservation:
            return []
        r = s.get(Reservation, criteres.idReservation)
        return [ReservationDTO.from_entity(r)] if r else []

# ----------------------------- CREATE (ancien, DTO complet) -------------
def creerReservation(dto: ReservationDTO) -> ReservationDTO:
    # validations minimales (gardent la compat tests)
    if dto.dateFin <= dto.dateDebut:
        raise ValueError("La date de fin doit être après la date de début.")
    if dto.prixParJour is None or float(dto.prixParJour) <= 0:
        raise ValueError("prixParJour doit être > 0.")
    if not dto.usager or not getattr(dto.usager, "idUsager", None):
        raise ValueError("UsagerDTO avec idUsager requis.")
    if not dto.chambre or not getattr(dto.chambre, "idChambre", None):
        raise ValueError("ChambreDTO avec idChambre requis.")

    with SessionLocal() as s:
        s: Session
        # Vérifie existence de l’usager et de la chambre.
        u = s.get(Usager, str(dto.usager.idUsager))
        ch = s.get(Chambre, str(dto.chambre.idChambre))
        if not u:
            raise ValueError("Usager introuvable.")
        if not ch:
            raise ValueError("Chambre introuvable.")

        # Construit l’entité ORM en gardant les types conformes (prix float).
        r = Reservation(
            date_debut_reservation=_naive(dto.dateDebut),
            date_fin_reservation=_naive(dto.dateFin),
            prix_jour=float(dto.prixParJour),   # modèle: MONEY/float
            info_reservation=dto.infoReservation,
            fk_id_usager=u.id_usager,
            fk_id_chambre=ch.id_chambre,
        )
        s.add(r)
        s.commit()
        s.refresh(r)
        return ReservationDTO.from_entity(r)

# ----------------------------- CREATE (nouveau, payload minimal) ---------
def creerReservationAvecIds(data: ReservationCreateDTO) -> ReservationDTO:
    """Crée une réservation avec seulement idUsager, idChambre, dates, prix, info."""
    # Garde les mêmes règles de base que la version legacy.
    if data.dateFin <= data.dateDebut:
        raise ValueError("La date de fin doit être après la date de début.")
    if data.prixParJour is None or float(data.prixParJour) <= 0:
        raise ValueError("prixParJour doit être > 0.")

    with SessionLocal() as s:
        s: Session
        u = s.get(Usager, str(data.idUsager))
        ch = s.get(Chambre, str(data.idChambre))
        if not u:
            raise ValueError("Usager introuvable.")
        if not ch:
            raise ValueError("Chambre introuvable.")

        r = Reservation(
            date_debut_reservation=_naive(data.dateDebut),
            date_fin_reservation=_naive(data.dateFin),
            prix_jour=float(data.prixParJour),
            info_reservation=data.infoReservation,
            fk_id_usager=u.id_usager,
            fk_id_chambre=ch.id_chambre,
        )
        s.add(r)
        s.commit()

        # Recharger avec relations pour retourner un DTO complet
        # (selectinload évite N+1, pis on est sûr d’avoir chambre+usager hydratés).
        r = s.execute(
            select(Reservation)
            .options(
                selectinload(Reservation.chambre).selectinload(Chambre.type_chambre),
                selectinload(Reservation.usager),
            )
            .where(Reservation.id_reservation == r.id_reservation)
        ).scalar_one()

        return ReservationDTO.from_entity(r)

# ----------------------------- UPDATE -----------------------------
def modifierReservation(id_reservation: str, data: ReservationUpdateDTO) -> ReservationDTO:
    with SessionLocal() as s:
        s: Session

        r = s.get(Reservation, id_reservation)
        if not r:
            raise ValueError("Réservation introuvable.")

        # Si on change l’usager, on vérifie qu’il existe.
        if data.idUsager:
            u = s.get(Usager, data.idUsager)
            if not u:
                raise ValueError("Usager introuvable.")
            r.fk_id_usager = u.id_usager

        # Idem pour la chambre.
        if data.idChambre:
            ch = s.get(Chambre, data.idChambre)
            if not ch:
                raise ValueError("Chambre introuvable.")
            r.fk_id_chambre = ch.id_chambre

        # Cohérence des dates au moment de l’update (début < fin).
        if data.dateDebut:
            if r.date_fin_reservation and data.dateDebut >= r.date_fin_reservation:
                raise ValueError("La date de début doit être avant la date de fin.")
            r.date_debut_reservation = _naive(data.dateDebut)

        if data.dateFin:
            if r.date_debut_reservation and data.dateFin <= r.date_debut_reservation:
                raise ValueError("La date de fin doit être après la date de début.")
            r.date_fin_reservation = _naive(data.dateFin)

        # ✅ Ajout: validation prixParJour > 0 à la mise à jour
        if data.prixParJour is not None:
            if float(data.prixParJour) <= 0:
                raise ValueError("prixParJour doit être > 0.")
            r.prix_jour = float(data.prixParJour)  # modèle: float

        # Note: infoReservation peut être None (on accepte).
        if data.infoReservation is not None:
            r.info_reservation = data.infoReservation

        s.commit()
        s.refresh(r)
        return ReservationDTO.from_entity(r)

# ----------------------------- DELETE -----------------------------
def supprimerReservation(id_reservation: str) -> bool:
    # Suppression « douce » : False si l’ID existe pas.
    with SessionLocal() as s:
        s: Session
        r = s.get(Reservation, id_reservation)
        if not r:
            return False
        s.delete(r)
        s.commit()
        return True
