# =====================================================================
# Test créer + lire réservation par ID (service “getReservationParId”)
# =====================================================================
import unittest
from datetime import datetime, timedelta
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from DTO.usagerDTO import UsagerCreateDTO
from DTO.reservationDTO import ReservationDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre
from metier.usagerMetier import creerUsager, supprimerUsager
from metier.reservationMetier import creerReservation, getReservationParId, supprimerReservation

class TestReservationService(unittest.TestCase):
    def test_creer_et_get_par_id(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Svc-RSV", prix_plancher=140.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=712, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        u = creerUsager(UsagerCreateDTO(prenom="Rémi", nom="Book", adresse="6 rue", mobile="333333333333333", mot_de_passe="x", type_usager="Usager"))

        r = creerReservation(ReservationDTO(dateDebut=datetime.utcnow(), dateFin=datetime.utcnow()+timedelta(days=2), prixParJour=150.0, infoReservation="Fenêtre", chambre=ch, usager=u))
        relu = getReservationParId(str(r.idReservation))
        self.assertIsNotNone(relu)
        self.assertEqual(relu.idReservation, r.idReservation)

        supprimerReservation(str(r.idReservation)); supprimerChambre(str(ch.idChambre)); supprimerTypeChambre(str(tc.idTypeChambre)); supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
