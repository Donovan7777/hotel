# =====================================================================
# Test recherche réservation par ID (legacy DTO de recherche)
# =====================================================================
import unittest
from datetime import datetime, timedelta
from DTO.chambreDTO import TypeChambreCreateDTO, ChambreCreateDTO
from DTO.usagerDTO import UsagerCreateDTO
from DTO.reservationDTO import ReservationDTO, CriteresRechercheDTO
from metier.chambreMetier import creerTypeChambre, creerChambre, supprimerChambre, supprimerTypeChambre
from metier.usagerMetier import creerUsager, supprimerUsager
from metier.reservationMetier import creerReservation, rechercherReservation, supprimerReservation

class TestReservationSearch(unittest.TestCase):
    def test_recherche_par_id(self):
        tc = creerTypeChambre(TypeChambreCreateDTO(nom_type="Search-RSV", prix_plancher=111.0, prix_plafond=None, description_chambre=""))
        ch = creerChambre(ChambreCreateDTO(numero_chambre=711, disponible_reservation=True, autre_informations="", nom_type=tc.nom_type))
        u = creerUsager(UsagerCreateDTO(prenom="Sara", nom="Rech", adresse="9 rue", mobile="666666666666666", mot_de_passe="x", type_usager="Usager"))
        r = creerReservation(ReservationDTO(dateDebut=datetime.utcnow(), dateFin=datetime.utcnow()+timedelta(days=1), prixParJour=145.0, infoReservation="", chambre=ch, usager=u))

        res = rechercherReservation(CriteresRechercheDTO(idReservation=str(r.idReservation)))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].idReservation, r.idReservation)

        supprimerReservation(str(r.idReservation)); supprimerChambre(str(ch.idChambre)); supprimerTypeChambre(str(tc.idTypeChambre)); supprimerUsager(str(u.idUsager))

if __name__ == "__main__":
    unittest.main()
