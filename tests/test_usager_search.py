# =====================================================================
# Test recherche d’un usager par ID (service rechercherUsager)
# - On crée un usager
# - On le retrouve via UsagerSearchDTO(idUsager=...)
# - On valide que la liste contient exactement cet usager
# =====================================================================
import unittest
from DTO.usagerDTO import UsagerCreateDTO, UsagerSearchDTO
from metier.usagerMetier import creerUsager, rechercherUsager, supprimerUsager

class TestUsagerSearch(unittest.TestCase):
    def test_rechercher_usager_par_id(self):
        # Arrange
        u = creerUsager(UsagerCreateDTO(
            prenom="Find",
            nom="Me",
            adresse="2 rue Recherche",
            mobile="888888888888888",
            mot_de_passe="secret",
            type_usager="Usager",
        ))
        try:
            # Act
            res = rechercherUsager(UsagerSearchDTO(idUsager=str(u.idUsager)))
            # Assert
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0].idUsager, u.idUsager)
        finally:
            # Clean
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
