# metier/usagerMetier.py
# -----------------------------------------------------------------------------
# Fichier: metier/usagerMetier.py
# Rôle : services métiers pour l’entité Usager (CRUD + mini dédoublonnage).
# Détails:
#   - creerUsager: petit check (nom+prenom+mobile) pour éviter des clones évidents.
#   - modifierUsager: patch champ par champ, normalise le mdp à 60 chars.
# -----------------------------------------------------------------------------

from __future__ import annotations

# Imports: on mélange ici ORM (Session, select) + types utilitaires (UUID)
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

# SessionLocal: fabrique de sessions DB; on ouvre/ferme par context manager
from core.db import SessionLocal

# Modèle ORM (table `usager`) et DTO (entrées/sorties côté API)
from modele.usager import Usager
from DTO.usagerDTO import UsagerDTO, UsagerCreateDTO, UsagerUpdateDTO, UsagerSearchDTO

# ------------------------------ CREATE -----------------------------
# Création d'un usager. On fait une vérif simple d'existence "métier"
# (nom + prénom + mobile) pour éviter de créer des doublons évidents.
def creerUsager(data: UsagerCreateDTO) -> UsagerDTO:
    with SessionLocal() as s:
        # Petit check anti-doublon: même nom/prénom/mobile => on retourne l'existant
        existing = s.execute(
            select(Usager).where(
                (Usager.nom == data.nom)
                & (Usager.prenom == data.prenom)
                & (Usager.mobile == data.mobile)
            )
        ).scalar_one_or_none()

        if existing:
            return UsagerDTO(existing)

        # Création de l'entité ORM à partir des champs du DTO
        # Note: mot_de_passe est normalisé à 60 char (padding) pour être conforme
        #       à une éventuelle colonne CHAR(60) / hash de longueur fixe.
        u = Usager(
            prenom=data.prenom,
            nom=data.nom,
            adresse=data.adresse,
            mobile=data.mobile,
            mot_de_passe=(data.mot_de_passe[:60]).ljust(60)[:60],
            type_usager=data.type_usager,
        )
        s.add(u)
        s.commit()     # Persisté en DB
        s.refresh(u)   # Recharge pour obtenir l'ID/valeurs générées
        return UsagerDTO(u)

# ------------------------------ READ ------------------------------
# Lecture ciblée par identifiant. On accepte `str` ou `UUID` pour être
# flexible côté appelants (ex.: provenant de la route ou du service).
def getUsagerParId(id_usager: str | UUID) -> UsagerDTO | None:
    with SessionLocal() as s:
        u = s.get(Usager, str(id_usager))
        return UsagerDTO(u) if u else None

# ------------------------------ LIST ------------------------------
# Listage complet, trié par nom puis prénom pour un affichage stable.
def listerUsagers() -> list[UsagerDTO]:
    with SessionLocal() as s:
        rows = s.execute(
            select(Usager).order_by(Usager.nom, Usager.prenom)
        ).scalars().all()
        return [UsagerDTO(u) for u in rows]

# -------------------------- SEARCH (ID) ---------------------------
# Compat/recherche minimaliste utilisée ailleurs: on prend un DTO de
# recherche, on s'attend à un idUsager, et on renvoie une liste (0/1).
def rechercherUsager(critere: UsagerSearchDTO) -> list[UsagerDTO]:
    with SessionLocal() as s:
        if not critere.idUsager:
            return []
        u = s.get(Usager, critere.idUsager)
        return [UsagerDTO(u)] if u else []

# ----------------------------- UPDATE -----------------------------
# Mise à jour partielle: on touche seulement aux champs fournis dans le DTO
# (pattern "patch-like"). Si un champ est None, on le laisse tel quel.
def modifierUsager(id_usager: str, data: UsagerUpdateDTO) -> UsagerDTO:
    with SessionLocal() as s:
        s: Session

        u = s.get(Usager, id_usager)
        if not u:
            raise ValueError("Usager introuvable.")

        if data.prenom is not None:
            u.prenom = data.prenom
        if data.nom is not None:
            u.nom = data.nom
        if data.adresse is not None:
            u.adresse = data.adresse
        if data.mobile is not None:
            u.mobile = data.mobile
        if data.mot_de_passe is not None:
            # Même normalisation à 60 char que lors de la création
            u.mot_de_passe = (data.mot_de_passe[:60]).ljust(60)[:60]
        if data.type_usager is not None:
            u.type_usager = data.type_usager

        s.commit()
        s.refresh(u)
        return UsagerDTO(u)

# ----------------------------- DELETE -----------------------------
# Suppression en douceur: si l'ID est inconnu, on retourne False.
# Sinon on supprime et on retourne True. Pas d'exception ici car c'est
# un cas d'usage attendu que l'ID puisse ne pas exister.
def supprimerUsager(id_usager: str) -> bool:
    with SessionLocal() as s:
        s: Session
        u = s.get(Usager, id_usager)
        if not u:
            return False
        s.delete(u)
        s.commit()
        return True
