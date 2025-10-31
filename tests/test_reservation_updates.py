# =====================================================================
# Test mise à jour d’une réservation (prix, dates, etc.)
# =====================================================================
import unittest
from datetime import datetime, timedelta
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from DTO.usagerDTO import UsagerCreateDTO
from DTO.reservationDTO import ReservationDTO, ReservationUpdateDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre
from metier.usagerMetier import creerUsager, supprimerUsager
from metier.reservationMetier import creerReservation, modifierReservation, supprimerReservation

class TestReservationUpdates(unittest.TestCase):
    def test_modifier_prix(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Upd-RSV", prix_plancher=120.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=713, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        u = creerUsager(UsagerCreateDTO(prenom="Julie", nom="Maj", adresse="7 rue", mobile="444444444444444", mot_de_passe="x", type_usager="Usager"))
        r = creerReservation(ReservationDTO(dateDebut=datetime.utcnow(), dateFin=datetime.utcnow()+timedelta(days=1), prixParJour=130.0, infoReservation="", chambre=ch, usager=u))

        maj = modifierReservation(str(r.idReservation), ReservationUpdateDTO(prixParJour=160.0))
        self.assertEqual(maj.prixParJour, 160.0)

        supprimerReservation(str(r.idReservation)); supprimerChambre(str(ch.idChambre)); supprimerTypeChambre(str(tc.idTypeChambre)); supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
