# =====================================================================
# Test suppression type de chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, supprimerTypeChambre

class TestTypeChambreDelete(unittest.TestCase):
    def test_supprimer_type(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Del-TC", prix_plancher=80.0, prix_plafond=None, description_chambre=None))
        ok = supprimerTypeChambre(str(tc.idTypeChambre))
        self.assertTrue(ok)

if __name__ == "__main__":
    unittest.main()
