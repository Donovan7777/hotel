# =====================================================================
# Test récupération par numéro de chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, getChambreParNumero, supprimerChambre, supprimerTypeChambre

class TestChambreByNumero(unittest.TestCase):
    def test_get_par_numero(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Num-CH", prix_plancher=100.0, prix_plafond=None, description_chambre=""))
        try:
            ch = creerChambre(ChambreCreateDTO(numero_chambre=704, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
            lu = getChambreParNumero(704)
            self.assertIsNotNone(lu)
            self.assertEqual(lu.idChambre, ch.idChambre)
        finally:
            if 'ch' in locals(): supprimerChambre(str(ch.idChambre))
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
