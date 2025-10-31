# =====================================================================
# Test listage des réservations
# =====================================================================
import unittest
from datetime import datetime, timedelta
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from DTO.usagerDTO import UsagerCreateDTO
from DTO.reservationDTO import ReservationDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre
from metier.usagerMetier import creerUsager, supprimerUsager
from metier.reservationMetier import creerReservation, listerReservations, supprimerReservation

class TestListerReservations(unittest.TestCase):
    def test_lister(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="List-RSV", prix_plancher=140.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=706, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        u = creerUsager(UsagerCreateDTO(prenom="Alex", nom="Liste", adresse="10 rue", mobile="777777777777777", mot_de_passe="x", type_usager="Usager"))
        try:
            r = creerReservation(ReservationDTO(
                dateDebut=datetime.utcnow(),
                dateFin=datetime.utcnow() + timedelta(days=2),
                prixParJour=150.0,
                infoReservation="",
                chambre=ch,
                usager=u
            ))
            lst = listerReservations()
            self.assertTrue(any(x.idReservation == r.idReservation for x in lst))
        finally:
            if 'r' in locals(): supprimerReservation(str(r.idReservation))
            supprimerChambre(str(ch.idChambre))
            supprimerTypeChambre(str(tc.idTypeChambre))
            supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
