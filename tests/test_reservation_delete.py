# =====================================================================
# Test suppression réservation
# =====================================================================
import unittest
from datetime import datetime, timedelta
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from DTO.usagerDTO import UsagerCreateDTO
from DTO.reservationDTO import ReservationDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre
from metier.usagerMetier import creerUsager, supprimerUsager
from metier.reservationMetier import creerReservation, supprimerReservation

class TestReservationDelete(unittest.TestCase):
    def test_supprimer_reservation(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Del-RSV", prix_plancher=100.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=710, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        u = creerUsager(UsagerCreateDTO(prenom="Marc", nom="Del", adresse="8 rue", mobile="555555555555555", mot_de_passe="x", type_usager="Usager"))
        r = creerReservation(ReservationDTO(dateDebut=datetime.utcnow(), dateFin=datetime.utcnow()+timedelta(days=1), prixParJour=100.0, infoReservation="", chambre=ch, usager=u))
        ok = supprimerReservation(str(r.idReservation))
        self.assertTrue(ok)
        supprimerChambre(str(ch.idChambre)); supprimerTypeChambre(str(tc.idTypeChambre)); supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
