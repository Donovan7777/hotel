# main.py
# -----------------------------------------------------------------------------
# Fichier: main.py
# Rôle : Application FastAPI (routes, CORS, wiring vers la couche métier).
# Notes:
#   - Les routes retournent les DTO (réponse propre).
#   - try/except ValueError -> lève HTTP 400 (bad request) avec message clair.
#   - POST /reservations accepte le payload minimal (IDs+dates+prix).
# -----------------------------------------------------------------------------

# FICHIER PRINCIPAL DE L’API
# - Ce fichier démarre l’app FastAPI et expose toutes les routes.
# - On reste simple et clair : chaque bloc est expliqué (CORS, DTO, routes).
# - Important : je n’ai RIEN changé au code existant sauf la route POST /reservations
#   qui accepte maintenant un payload minimal (IDs + dates + prix).

"""
Application principale FastAPI pour gérer les chambres, les types de chambres,
les usagers et les réservations d'hôtel.

Pour lancer le serveur :
    uvicorn main:app --reload

Docs :
    http://127.0.0.1:8000/docs
"""

# ------------------- Imports de base FastAPI -------------------
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

# ------------------- DTOs (validation/retour) -------------------
from DTO.chambreDTO import (
    ChambreDTO,
    TypeChambreDTO,
    TypeChambreCreateDTO,
    TypeChambreUpdateDTO,
    ChambreCreateDTO,
    ChambreUpdateDTO,
)
from DTO.reservationDTO import (
    ReservationDTO,
    ReservationCreateDTO,   # <-- import du payload minimal
    ReservationUpdateDTO,
)
from DTO.usagerDTO import (
    UsagerDTO,
    UsagerCreateDTO,
    UsagerUpdateDTO,
)

# ------------------- Couche métier (logique) -------------------
from metier.chambreMetier import (
    creerChambre,
    creerTypeChambre,
    getChambreParNumero,
    listerChambres,
    listerTypesChambre,
    modifierChambre,
    supprimerChambre,
    modifierTypeChambre,
    supprimerTypeChambre,
    rechercherChambreParId,   # GET par ID pour les chambres
    getTypeChambreParId,      # GET par ID pour les types de chambre
)
from metier.reservationMetier import (
    listerReservations,       # GET list des réservations
    getReservationParId,      # GET par ID pour une réservation
    creerReservationAvecIds,  # <-- nouvelle fonction (payload minimal)
    modifierReservation,
    supprimerReservation,
)
from metier.usagerMetier import (
    creerUsager,
    modifierUsager,
    supprimerUsager,
    getUsagerParId,           # GET par ID pour un usager
    listerUsagers,            # GET list des usagers
)

# ------------------- App & CORS -------------------
app = FastAPI(
    title="API Hôtel - Projet Partiel",
    description="API permettant de gérer les chambres, les usagers et les réservations d'un hôtel.",
    version="1.0.0",
)

# CORS large pour dev. En prod, je restreindrais ça aux domaines connus.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # En prod: restreindre aux domaines connus
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Utilitaires -------------------
@app.get("/", summary="Statut de l'API")
def root():
    # Petit endpoint santé (simple).
    return {"status": "ok", "docs": "/docs"}

@app.get("/health", summary="Vérification de santé")
def health():
    # Un autre ping santé si jamais pour monitoring.
    return {"status": "ok"}

# ===================================================
#                ROUTES - CHAMBRES
# ===================================================
@app.get(
    "/chambres/{no_chambre}",
    response_model=ChambreDTO,
    summary="Obtenir une chambre par numéro",
    description="Retourne les infos complètes d'une chambre selon son numéro (ex.: 101).",
)
def api_get_chambre(no_chambre: int):
    ch = getChambreParNumero(no_chambre)
    if not ch:
        raise HTTPException(status_code=404, detail=f"Chambre {no_chambre} non trouvée.")
    return ch

@app.get(
    "/chambres",
    response_model=list[ChambreDTO],
    summary="Lister les chambres",
    description="Retourne la liste de toutes les chambres (tri simple par numéro).",
)
def api_lister_chambres():
    return listerChambres()

@app.get(
    "/chambres/id/{id_chambre}",
    response_model=ChambreDTO,
    summary="Rechercher une chambre par ID",
    description="Retourne une chambre selon son identifiant (UUID).",
)
def api_rechercher_chambre_par_id(id_chambre: str):
    ch = rechercherChambreParId(id_chambre)
    if not ch:
        raise HTTPException(status_code=404, detail="Chambre introuvable.")
    return ch

@app.post(
    "/creerChambre",
    response_model=ChambreDTO,
    summary="Créer une chambre",
    description="Ajoute une chambre en liant un type existant via son nom (nom_type).",
)
def api_creer_chambre(body: ChambreCreateDTO):
    try:
        return creerChambre(body)
    except ValueError as e:
        # Transforme en 400 côté client avec le message métier.
        raise HTTPException(status_code=400, detail=str(e))

@app.put(
    "/chambres/{id_chambre}",
    response_model=ChambreDTO,
    summary="Modifier une chambre",
    description="Modifie partiellement (numéro, dispo, infos, type via nom).",
)
def api_modifier_chambre(id_chambre: str, body: ChambreUpdateDTO):
    try:
        return modifierChambre(id_chambre, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete(
    "/chambres/{id_chambre}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une chambre",
    description="Supprime une chambre (échec si des réservations y sont rattachées).",
)
def api_supprimer_chambre(id_chambre: str):
    try:
        ok = supprimerChambre(id_chambre)
        if not ok:
            raise HTTPException(status_code=404, detail="Chambre introuvable.")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===================================================
#            ROUTES - TYPES DE CHAMBRE
# ===================================================
@app.get(
    "/typesChambre",
    response_model=list[TypeChambreDTO],
    summary="Lister les types de chambre",
    description="Retourne la liste des types de chambre (simple, double, etc.).",
)
def api_lister_types_chambre():
    return listerTypesChambre()

@app.get(
    "/typeChambre/{id_type_chambre}",
    response_model=TypeChambreDTO,
    summary="Obtenir un type de chambre par ID",
    description="Retourne un type de chambre selon son identifiant (UUID).",
)
def api_get_type_chambre_by_id(id_type_chambre: str):
    tc = getTypeChambreParId(id_type_chambre)
    if not tc:
        raise HTTPException(status_code=404, detail="Type de chambre introuvable.")
    return tc

@app.post(
    "/creerTypeChambre",
    response_model=TypeChambreDTO,
    summary="Créer un type de chambre",
    description="Ajoute un nouveau type (nom, prix plancher/plafond, description).",
)
def api_creer_type_chambre(body: TypeChambreCreateDTO):
    return creerTypeChambre(body)

@app.put(
    "/typeChambre/{id_type_chambre}",
    response_model=TypeChambreDTO,
    summary="Modifier un type de chambre",
    description="Modifie nom/prix/description du type de chambre.",
)
def api_modifier_type_chambre(id_type_chambre: str, body: TypeChambreUpdateDTO):
    try:
        return modifierTypeChambre(id_type_chambre, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete(
    "/typeChambre/{id_type_chambre}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un type de chambre",
    description="Échoue si des chambres dépendent encore de ce type.",
)
def api_supprimer_type_chambre(id_type_chambre: str):
    try:
        ok = supprimerTypeChambre(id_type_chambre)
        if not ok:
            raise HTTPException(status_code=404, detail="Type de chambre introuvable.")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ===================================================
#               ROUTES - RÉSERVATIONS
# ===================================================
@app.get(
    "/reservations",
    response_model=list[ReservationDTO],
    summary="Lister les réservations",
    description="Retourne la liste de toutes les réservations (tri par date de début).",
)
def api_lister_reservations():
    return listerReservations()

@app.get(
    "/reservations/{id_reservation}",
    response_model=ReservationDTO,
    summary="Obtenir une réservation par ID",
    description="Retourne une réservation selon son identifiant (UUID).",
)
def api_get_reservation_by_id(id_reservation: str):
    r = getReservationParId(id_reservation)
    if not r:
        raise HTTPException(status_code=404, detail="Réservation introuvable.")
    return r

# ✅ NOUVEAU: payload minimal (IDs + dates + prix [+ note])
@app.post(
    "/reservations",
    response_model=ReservationDTO,
    summary="Créer une réservation (payload minimal par IDs)",
    description=("Body minimal: idUsager, idChambre, dateDebut, dateFin, "
                 "prixParJour, infoReservation (optionnel). Réponse: DTO complet."),
)
def api_creer_reservation_simple(body: ReservationCreateDTO):
    try:
        return creerReservationAvecIds(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put(
    "/reservations/{id_reservation}",
    response_model=ReservationDTO,
    summary="Modifier une réservation",
    description="Modifie partiellement une réservation (dates, prix, chambre/usager, infos).",
)
def api_modifier_reservation(id_reservation: str, body: ReservationUpdateDTO):
    try:
        return modifierReservation(id_reservation, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete(
    "/reservations/{id_reservation}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une réservation",
    description="Supprime une réservation existante.",
)
def api_supprimer_reservation(id_reservation: str):
    ok = supprimerReservation(id_reservation)
    if not ok:
        raise HTTPException(status_code=404, detail="Réservation introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ===================================================
#                 ROUTES - USAGERS
# ===================================================
@app.get(
    "/usagers",
    response_model=list[UsagerDTO],
    summary="Lister les usagers",
    description="Retourne la liste de tous les usagers.",
)
def api_lister_usagers():
    return listerUsagers()

@app.post(
    "/usagers",
    response_model=UsagerDTO,
    summary="Créer un usager",
    description="Ajoute un usager (petit dédoublonnage nom+prénom+mobile).",
)
def api_creer_usager(body: UsagerCreateDTO):
    try:
        return creerUsager(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get(
    "/usagers/{id_usager}",
    response_model=UsagerDTO,
    summary="Obtenir un usager",
    description="Retourne un usager par son identifiant (UUID).",
)
def api_get_usager(id_usager: str):
    u = getUsagerParId(id_usager)
    if not u:
        raise HTTPException(status_code=404, detail="Usager introuvable.")
    return u

@app.put(
    "/usagers/{id_usager}",
    response_model=UsagerDTO,
    summary="Modifier un usager",
    description="Modifie partiellement un usager (tous les champs sauf l'ID).",
)
def api_modifier_usager(id_usager: str, body: UsagerUpdateDTO):
    try:
        return modifierUsager(id_usager, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete(
    "/usagers/{id_usager}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un usager",
    description="Supprime un usager.",
)
def api_supprimer_usager(id_usager: str):
    ok = supprimerUsager(id_usager)
    if not ok:
        raise HTTPException(status_code=404, detail="Usager introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ------------------- Entrée locale -------------------
if __name__ == "__main__":
    import uvicorn
    # Démarrage local en dev. reload=True pour hot-reload (pratique).
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
