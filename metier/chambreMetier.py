# metier/chambreMetier.py
# -----------------------------------------------------------------------------
# Fichier: metier/chambreMetier.py
# Rôle : logique métier pour TypeChambre et Chambre (CRUD + validations).
# Points d’attention:
#   - _ensure_plafond_ok: s’assure que prix_plafond est numérique (string) et
#     >= prix_plancher si fourni. Ça respecte le modèle (plafond en NCHAR(10)).
#   - On relie Chambre -> TypeChambre par nom_type pour la création/maj (simple).
#   - Gestion d’erreurs ValueError pour renvoyer 400 côté API.
# -----------------------------------------------------------------------------

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.db import SessionLocal
from DTO.chambreDTO import (
    ChambreDTO,
    TypeChambreDTO,
    TypeChambreCreateDTO,
    TypeChambreUpdateDTO,
    ChambreCreateDTO,
    ChambreUpdateDTO,
    TypeChambreSearchDTO,
)
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre

def _ensure_plafond_ok(plancher: float | None, plafond_str: str | None) -> None:
    """Si prix_plafond (string) est fourni, vérifier que c'est numérique
    et, si prix_plancher est fourni, que plafond >= plancher."""
    # Ici je tolère None (pas de plafond), sinon je parse avec Decimal (plus strict).
    if plafond_str is None:
        return
    try:
        plafond = Decimal(plafond_str.strip().replace(",", "."))
    except (InvalidOperation, AttributeError):
        raise ValueError("prix_plafond doit être un nombre valide (ex: '199.99').")

    if plancher is not None:
        plancher_dec = Decimal(str(plancher))
        if plafond < plancher_dec:
            raise ValueError("Le prix plafond doit être supérieur ou égal au prix plancher.")

# ----------------------------- CREATE -----------------------------
def creerTypeChambre(data: TypeChambreCreateDTO) -> TypeChambreDTO:
    # Je vérifie si le nom existe déjà pour éviter doublon plate.
    with SessionLocal() as session:
        exists = session.execute(
            select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
        ).scalar_one_or_none()
        if exists:
            return TypeChambreDTO(exists)

        # Valide le plafond (string) vs plancher (float).
        _ensure_plafond_ok(data.prix_plancher, data.prix_plafond)

        # Création, commit, refresh pour récupérer l’ID.
        new_tc = TypeChambre(
            nom_type=data.nom_type,
            prix_plancher=data.prix_plancher,       # modèle: float (MONEY)
            prix_plafond=data.prix_plafond,         # modèle: str (NCHAR(10))
            description_chambre=data.description_chambre,
        )
        session.add(new_tc)
        session.commit()
        session.refresh(new_tc)
        return TypeChambreDTO(new_tc)

def creerChambre(data: ChambreCreateDTO) -> ChambreDTO:
    with SessionLocal() as session:
        # On resolve le type par son nom pour lier proprement (FK).
        tc = session.execute(
            select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
        ).scalar_one_or_none()
        if tc is None:
            raise ValueError(f"Type de chambre '{data.nom_type}' introuvable.")

        ch = Chambre(
            numero_chambre=data.numero_chambre,
            disponible_reservation=data.disponible_reservation,
            autre_informations=data.autre_informations,
            type_chambre=tc,
        )
        session.add(ch)
        session.commit()
        session.refresh(ch)
        return ChambreDTO(ch)

# --------------------------- READ / LIST ---------------------------
def getChambreParNumero(no_chambre: int) -> ChambreDTO | None:
    # Recherche par numero_chambre (ex.: 101).
    with SessionLocal() as session:
        ch = session.execute(
            select(Chambre).where(Chambre.numero_chambre == no_chambre)
        ).scalar_one_or_none()
        return ChambreDTO(ch) if ch else None

def listerTypesChambre() -> List[TypeChambreDTO]:
    # Trié par nom pour le confort visuel dans un drop-down.
    with SessionLocal() as session:
        rows = session.execute(
            select(TypeChambre).order_by(TypeChambre.nom_type)
        ).scalars().all()
        return [TypeChambreDTO(t) for t in rows]

def listerChambres() -> List[ChambreDTO]:
    # Tri par numéro pour un listing clean.
    with SessionLocal() as session:
        rows = session.execute(
            select(Chambre).order_by(Chambre.numero_chambre)
        ).scalars().all()
        return [ChambreDTO(c) for c in rows]

# ---------------------------- SEARCH (ID) --------------------------
def rechercherChambreParId(id_chambre: str) -> ChambreDTO | None:
    # Fetch direct par PK (UUID).
    with SessionLocal() as session:
        ch = session.get(Chambre, id_chambre)
        return ChambreDTO(ch) if ch else None

def getTypeChambreParId(id_type_chambre: str) -> TypeChambreDTO | None:
    with SessionLocal() as session:
        tc = session.get(TypeChambre, id_type_chambre)
        return TypeChambreDTO(tc) if tc else None

def rechercherTypeChambre(critere: TypeChambreSearchDTO) -> List[TypeChambreDTO]:
    # Je garde ça minimaliste pour matcher la consigne.
    with SessionLocal() as session:
        if not critere.idTypeChambre:
            return []
        tc = session.get(TypeChambre, critere.idTypeChambre)
        return [TypeChambreDTO(tc)] if tc else []

# ------------------------------ UPDATE ----------------------------
def modifierTypeChambre(id_type_chambre: str, data: TypeChambreUpdateDTO) -> TypeChambreDTO:
    with SessionLocal() as session:
        session: Session
        tc = session.get(TypeChambre, id_type_chambre)
        if not tc:
            raise ValueError("Type de chambre introuvable.")

        # On valide le plafond vs plancher (en tenant compte des valeurs actuelles).
        plancher = data.prix_plancher if data.prix_plancher is not None else float(tc.prix_plancher)
        plafond_str = data.prix_plafond if data.prix_plafond is not None else tc.prix_plafond
        _ensure_plafond_ok(plancher, plafond_str)

        # Patch champ par champ.
        if data.nom_type is not None:
            tc.nom_type = data.nom_type
        if data.prix_plancher is not None:
            tc.prix_plancher = data.prix_plancher
        if data.prix_plafond is not None:
            tc.prix_plafond = data.prix_plafond
        if data.description_chambre is not None:
            tc.description_chambre = data.description_chambre

        session.commit()
        session.refresh(tc)
        return TypeChambreDTO(tc)

def modifierChambre(id_chambre: str, data: ChambreUpdateDTO) -> ChambreDTO:
    with SessionLocal() as session:
        session: Session
        ch = session.get(Chambre, id_chambre)
        if not ch:
            raise ValueError("Chambre introuvable.")

        # Patch simple des champs scalaires.
        if data.numero_chambre is not None:
            ch.numero_chambre = data.numero_chambre
        if data.disponible_reservation is not None:
            ch.disponible_reservation = data.disponible_reservation
        if data.autre_informations is not None:
            ch.autre_informations = data.autre_informations

        # Si on change de type, on résout par nom_type (doit exister).
        if data.nom_type is not None:
            tc = session.execute(
                select(TypeChambre).where(TypeChambre.nom_type == data.nom_type)
            ).scalar_one_or_none()
            if not tc:
                raise ValueError(f"Type de chambre '{data.nom_type}' introuvable.")
            ch.fk_type_chambre = tc.id_type_chambre
            ch.type_chambre = tc

        session.commit()
        session.refresh(ch)
        return ChambreDTO(ch)

# ------------------------------ DELETE ----------------------------
def supprimerTypeChambre(id_type_chambre: str) -> bool:
    with SessionLocal() as session:
        session: Session
        tc = session.get(TypeChambre, id_type_chambre)
        if not tc:
            return False
        try:
            session.delete(tc)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            # Message clair si FK bloque.
            raise ValueError(
                "Impossible de supprimer ce type de chambre car des chambres y sont rattachées."
            )

def supprimerChambre(id_chambre: str) -> bool:
    with SessionLocal() as session:
        session: Session
        ch = session.get(Chambre, id_chambre)
        if not ch:
            return False
        try:
            session.delete(ch)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            # Pareil: empêche si réservations existent.
            raise ValueError(
                "Impossible de supprimer cette chambre car des réservations y sont rattachées."
            )
