# =====================================================================
# Test suppression d’un usager
# - On crée un usager
# - On le supprime via le service
# - On vérifie que la suppression retourne True
# =====================================================================
import unittest
from DTO.usagerDTO import UsagerCreateDTO
from metier.usagerMetier import creerUsager, supprimerUsager, getUsagerParId

class TestUsagerDelete(unittest.TestCase):
    def test_supprimer_usager(self):
        # Arrange — créer un usager jetable
        u = creerUsager(UsagerCreateDTO(
            prenom="Del",
            nom="User",
            adresse="1 rue Jetable",
            mobile="999999999999999",
            mot_de_passe="secret",
            type_usager="Usager",
        ))
        # Act
        ok = supprimerUsager(str(u.idUsager))
        # Assert
        self.assertTrue(ok)
        # Et s’il reste quelque chose (devrait pas), on nettoie
        relu = getUsagerParId(str(u.idUsager))
        if relu is not None:
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
