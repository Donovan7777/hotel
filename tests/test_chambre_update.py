# =====================================================================
# Test mise à jour partielle d’une chambre
# =====================================================================
import unittest
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO, ChambreUpdateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, modifierChambre, supprimerChambre, supprimerTypeChambre

class TestChambreUpdate(unittest.TestCase):
    def test_modifier_chambre_infos(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Upd-CH", prix_plancher=120.0, prix_plafond=None, description_chambre=""))
        try:
            ch = creerChambre(ChambreCreateDTO(numero_chambre=703, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
            maj = modifierChambre(str(ch.idChambre), ChambreUpdateDTO(autre_informations="Vue sur jardin"))
            self.assertEqual(maj.autre_informations, "Vue sur jardin")
        finally:
            if 'ch' in locals(): supprimerChambre(str(ch.idChambre))
            supprimerTypeChambre(str(tc.idTypeChambre))

if __name__ == "__main__":
    unittest.main()
