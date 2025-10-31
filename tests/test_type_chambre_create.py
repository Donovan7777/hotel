# =====================================================================
# Test création type de chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, supprimerTypeChambre

class TestTypeChambreCreate(unittest.TestCase):
    def test_creer_type(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Create-TC", prix_plancher=79.99, prix_plafond=None, description_chambre="Éco"))
        self.assertIsNotNone(tc.idTypeChambre)
        self.assertEqual(tc.nom_type, "Create-TC")
        supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
