# DTO/chambreDTO.py
# -----------------------------------------------------------------------------
# Fichier: DTO/chambreDTO.py
# Rôle : objets de transfert pour TypeChambre et Chambre.
# Idée: ces DTO sortent des routes (réponse API) et servent aussi pour valider
#       des entrées (create/update). J’ai mis des Field(...) pour limiter tailles.
# Note: TypeChambre.prix_plafond est un str en DB (NCHAR(10)), je le garde pareil
#       ici pour être fidèle au modèle, mais je convertis prix_plancher en float.
# -----------------------------------------------------------------------------

from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from modele.chambre import Chambre
from modele.type_chambre import TypeChambre

# -------------------- OUTPUT DTOs --------------------
# Ce DTO est celui qu’on retourne côté API quand on parle d’un type de chambre.
class TypeChambreDTO(BaseModel):
    idTypeChambre: UUID
    nom_type: str
    prix_plafond: Optional[str] = None
    prix_plancher: float
    description_chambre: Optional[str] = None

    # constructeur à partir de l'entité modèle
    # Tip: j’fais la conversion money->float ici (prix_plancher).
    def __init__(self, typeChambre: TypeChambre):
        super().__init__(
            idTypeChambre=typeChambre.id_type_chambre,
            nom_type=typeChambre.nom_type,
            prix_plafond=typeChambre.prix_plafond,
            prix_plancher=float(typeChambre.prix_plancher),
            description_chambre=typeChambre.description_chambre,
        )

# Ce DTO résume une chambre. J’imbrique le TypeChambreDTO si la relation est chargée.
class ChambreDTO(BaseModel):
    idChambre: UUID
    numero_chambre: int
    disponible_reservation: bool
    autre_informations: Optional[str] = None
    # ⬇️ make it optional so listing works even if the relationship isn't loaded
    type_chambre: Optional[TypeChambreDTO] = None

    # constructeur à partir de l'entité modèle (imbrique le TypeChambreDTO si présent)
    # If: getattr(..., None) évite un crash si la relation n’est pas chargée (lazy).
    def __init__(self, chambre: Chambre):
        super().__init__(
            idChambre=chambre.id_chambre,
            numero_chambre=chambre.numero_chambre,
            disponible_reservation=chambre.disponible_reservation,
            autre_informations=chambre.autre_informations,
            type_chambre=TypeChambreDTO(chambre.type_chambre) if getattr(chambre, "type_chambre", None) else None,
        )

# -------------------- INPUT DTOs --------------------
# Create DTO pour TypeChambre: je mets max_length pour garder ça clean.
class TypeChambreCreateDTO(BaseModel):
    nom_type: str = Field(min_length=1, max_length=50)
    prix_plancher: float
    prix_plafond: Optional[str] = Field(default=None, max_length=10)
    description_chambre: Optional[str] = Field(default=None, max_length=200)

# Update DTO: tout est optionnel (patch partiel). On valide tailles pareil.
class TypeChambreUpdateDTO(BaseModel):
    nom_type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    prix_plancher: Optional[float] = None
    prix_plafond: Optional[str] = Field(default=None, max_length=10)
    description_chambre: Optional[str] = Field(default=None, max_length=200)

# Create DTO pour Chambre: on lie au type par son nom (plus simple côté UI).
class ChambreCreateDTO(BaseModel):
    numero_chambre: int
    disponible_reservation: bool
    autre_informations: Optional[str] = None
    nom_type: str = Field(min_length=1, max_length=50)  # référence par nom

# Update DTO pour Chambre: tout est optionnel (on set juste ce qui change).
class ChambreUpdateDTO(BaseModel):
    numero_chambre: Optional[int] = None
    disponible_reservation: Optional[bool] = None
    autre_informations: Optional[str] = None
    nom_type: Optional[str] = Field(default=None, min_length=1, max_length=50)

# -------------------- SEARCH DTOs --------------------
# Petit DTO pour rechercher par ID, utile pour routes simples (GET id).
class TypeChambreSearchDTO(BaseModel):
    idTypeChambre: Optional[str] = Field(default=None, min_length=36, max_length=36)
    nom_type: Optional[str] = Field(default=None, max_length=50)
