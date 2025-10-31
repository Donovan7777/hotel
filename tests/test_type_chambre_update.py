# =====================================================================
# Test mise à jour complète d’un type de chambre
# =====================================================================
import unittest, uuid
from sqlalchemy import select
from core.db import SessionLocal
from DTO.chambreDTO import TypeChambreCreateDTO, TypeChambreUpdateDTO
from metier.chambreMetier import creerTypeChambre, modifierTypeChambre
from modele.type_chambre import TypeChambre

class TestTypeChambreUpdate(unittest.TestCase):
    def test_modifier_fields(self):
        base = f"tc-{uuid.uuid4().hex[:6]}"
        _ = creerTypeChambre(TypeChambreCreateDTO(nom_type=base, prix_plancher=70.0, prix_plafond="200", description_chambre="old"))
        with SessionLocal() as s:
            ent = s.execute(select(TypeChambre).where(TypeChambre.nom_type == base)).scalar_one_or_none()
            self.assertIsNotNone(ent)
            id_type = str(ent.id_type_chambre)

        updated = modifierTypeChambre(id_type, TypeChambreUpdateDTO(nom_type=f"{base}-n", prix_plancher=99.5, prix_plafond="300", description_chambre="new"))
        self.assertEqual(updated.nom_type, f"{base}-n")
        self.assertEqual(float(updated.prix_plancher), 99.5)
        self.assertEqual((updated.prix_plafond or "").strip(), "300")
        self.assertEqual(updated.description_chambre, "new")

if __name__ == "__main__":
    unittest.main()
