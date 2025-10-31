# DTO/usagerDTO.py
# -----------------------------------------------------------------------------
# Fichier: DTO/usagerDTO.py
# Rôle : DTO pour Usager (sortie + create/update + petit search).
# Notes: le constructeur principal prend un modèle Usager ORM
#        et sort un DTO propre pour l’API.
# -----------------------------------------------------------------------------

from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from modele.usager import Usager

# -------------------- OUTPUT DTO --------------------
# DTO retourné vers le client. Pas de mot_de_passe ici (normal).
class UsagerDTO(BaseModel):
    idUsager: UUID
    prenom: str
    nom: str
    adresse: str
    mobile: str
    type_usager: str

    # constructeur à partir de l'entité modèle
    # Simple mapping champ à champ (sans le mdp, évidemment!).
    def __init__(self, usager: Usager):
        super().__init__(
            idUsager=usager.id_usager,
            prenom=usager.prenom,
            nom=usager.nom,
            adresse=usager.adresse,
            mobile=usager.mobile,
            type_usager=usager.type_usager,
        )

# -------------------- INPUT DTOs --------------------
# Create DTO: validations basiques (longueurs), rien de fancy.
class UsagerCreateDTO(BaseModel):
    prenom: str = Field(min_length=1, max_length=50)
    nom: str = Field(min_length=1, max_length=50)
    adresse: str = Field(min_length=1, max_length=100)
    mobile: str = Field(min_length=1, max_length=15)
    mot_de_passe: str = Field(min_length=1, max_length=60)
    type_usager: str = Field(min_length=1, max_length=50)

# Update DTO: patch partiel, mêmes limites de tailles.
class UsagerUpdateDTO(BaseModel):
    prenom: Optional[str] = Field(default=None, min_length=1, max_length=50)
    nom: Optional[str] = Field(default=None, min_length=1, max_length=50)
    adresse: Optional[str] = Field(default=None, min_length=1, max_length=100)
    mobile: Optional[str] = Field(default=None, min_length=1, max_length=15)
    mot_de_passe: Optional[str] = Field(default=None, min_length=1, max_length=60)
    type_usager: Optional[str] = Field(default=None, min_length=1, max_length=50)

# -------------------- SEARCH DTO --------------------
# Petit DTO utilitaire pour fetch un user par ID ou filtrer sommaire.
class UsagerSearchDTO(BaseModel):
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    prenom: Optional[str] = None
    nom: Optional[str] = None
    type_usager: Optional[str] = None
