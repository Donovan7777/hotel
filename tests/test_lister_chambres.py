# =====================================================================
# Test listage des chambres
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, listerChambres, supprimerChambre, supprimerTypeChambre

class TestListerChambres(unittest.TestCase):
    def test_lister(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="List-CH", prix_plancher=95.0, prix_plafond=None, description_chambre=""))
        try:
            ch = creerChambre(ChambreCreateDTO(numero_chambre=705, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
            lst = listerChambres()
            self.assertTrue(any(x.idChambre == ch.idChambre for x in lst))
        finally:
            if 'ch' in locals(): supprimerChambre(str(ch.idChambre))
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
