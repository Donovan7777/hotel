# =====================================================================
# Test création usager + get par ID
# =====================================================================
import unittest
from DTO.usagerDTO import UsagerCreateDTO
from metier.usagerMetier import creerUsager, getUsagerParId, supprimerUsager

class TestUsagerCreate(unittest.TestCase):
    def test_creer_et_get(self):
        u = creerUsager(UsagerCreateDTO(prenom="Jean", nom="Tremblay", adresse="1000 rue", mobile="111111111111111", mot_de_passe="secret", type_usager="Usager"))
        try:
            relu = getUsagerParId(str(u.idUsager))
            self.assertIsNotNone(relu)
            self.assertEqual(relu.idUsager, u.idUsager)
        finally:
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
