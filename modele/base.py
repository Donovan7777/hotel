# modele/base.py
# -----------------------------------------------------------------------------
# Fichier: modele/base.py
# Rôle : Base déclarative SQLAlchemy. Tous les modèles héritent de ça.
# -----------------------------------------------------------------------------

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass  # Rien d’autre ici, c’est correct. On garde ça simple.
