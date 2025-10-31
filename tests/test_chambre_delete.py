# =====================================================================
# Test suppression de chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre

class TestChambreDelete(unittest.TestCase):
    def test_supprimer_chambre(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="ToDel-CH", prix_plancher=90.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=702, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        ok = supprimerChambre(str(ch.idChambre))
        self.assertTrue(ok)
        supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
