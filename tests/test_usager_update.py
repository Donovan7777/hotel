# =====================================================================
# Test mise à jour partielle d’un usager
# - On crée un usager
# - On modifie quelques champs (adresse, mobile, type_usager)
# - On vérifie que seuls ces champs ont changé
# =====================================================================
import unittest
from DTO.usagerDTO import UsagerCreateDTO, UsagerUpdateDTO
from metier.usagerMetier import creerUsager, modifierUsager, getUsagerParId, supprimerUsager

class TestUsagerUpdate(unittest.TestCase):
    def test_modifier_usager(self):
        # Arrange — création
        u = creerUsager(UsagerCreateDTO(
            prenom="Julie",
            nom="Lavoie",
            adresse="3 rue Avant",
            mobile="777777777777777",
            mot_de_passe="mdp",
            type_usager="Usager",
        ))
        try:
            # Act — mise à jour partielle
            maj = modifierUsager(
                str(u.idUsager),
                UsagerUpdateDTO(
                    adresse="33 rue Après",
                    mobile="123456789012345",
                    type_usager="Admin",
                ),
            )
            # Assert — champs modifiés
            self.assertEqual(maj.adresse, "33 rue Après")
            self.assertEqual(maj.mobile, "123456789012345")
            self.assertEqual(maj.type_usager, "Admin")
            # Et les champs non touchés restent tels quels
            self.assertEqual(maj.prenom, "Julie")
            self.assertEqual(maj.nom, "Lavoie")

            # Double-check en relisant depuis la BD
            relu = getUsagerParId(str(u.idUsager))
            self.assertIsNotNone(relu)
            self.assertEqual(relu.adresse, "33 rue Après")
            self.assertEqual(relu.mobile, "123456789012345")
            self.assertEqual(relu.type_usager, "Admin")
        finally:
            # Clean
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
