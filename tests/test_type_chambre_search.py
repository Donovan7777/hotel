# =====================================================================
# Test recherche type de chambre par ID (legacy DTO search)
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, TypeChambreSearchDTO
from metier.chambreMetier import creerTypeChambre, rechercherTypeChambre, supprimerTypeChambre

class TestTypeChambreSearch(unittest.TestCase):
    def test_rechercher_par_id(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Search-TC", prix_plancher=120.0, prix_plafond=None, description_chambre=""))
        try:
            res = rechercherTypeChambre(TypeChambreSearchDTO(idTypeChambre=str(tc.idTypeChambre)))
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0].idTypeChambre, tc.idTypeChambre)
        finally:
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
