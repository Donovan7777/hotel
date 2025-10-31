# =====================================================================
# Test création de chambre (service métier)
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre

class TestChambreCreate(unittest.TestCase):
    def test_creer_chambre_ok(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Create-CH", prix_plancher=80.0, prix_plafond=None, description_chambre=""))
        try:
            ch = creerChambre(ChambreCreateDTO(numero_chambre=701, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
            self.assertIsNotNone(ch.idChambre)
            self.assertEqual(ch.numero_chambre, 701)
        finally:
            # clean
            if 'ch' in locals(): supprimerChambre(str(ch.idChambre))
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
