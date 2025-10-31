# =====================================================================
# Test listage types de chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, listerTypesChambre, supprimerTypeChambre

class TestListerTypesChambre(unittest.TestCase):
    def test_lister_types(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="List-TC", prix_plancher=99.0, prix_plafond=None, description_chambre=""))
        try:
            lst = listerTypesChambre()
            self.assertTrue(any(x.idTypeChambre == tc.idTypeChambre for x in lst))
        finally:
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
