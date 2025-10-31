# =====================================================================
# Test listage usagers
# =====================================================================
import unittest
from DTO.usagerDTO import UsagerCreateDTO
from metier.usagerMetier import creerUsager, listerUsagers, supprimerUsager

class TestListerUsager(unittest.TestCase):
    def test_lister(self):
        u = creerUsager(UsagerCreateDTO(prenom="List", nom="User", adresse="1 rue", mobile="222222222222222", mot_de_passe="x", type_usager="Usager"))
        try:
            lst = listerUsagers()
            self.assertTrue(any(x.idUsager == u.idUsager for x in lst))
        finally:
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
