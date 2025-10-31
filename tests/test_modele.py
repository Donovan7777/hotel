# ==============================================================
# test_full_integration.py
# Tests d’intégration complets pour vérifier que tous les modèles
# fonctionnent ensemble : TypeChambre, Chambre, Usager, Réservation.
# Ces tests simulent un scénario réel de création et de relation
# entre les différentes tables du projet hôtel.
# ==============================================================

import unittest
from datetime import datetime, timedelta
from sqlalchemy import select

from core.db import SessionLocal, init_db
from modele.type_chambre import TypeChambre
from modele.chambre import Chambre
from modele.usager import Usager
from modele.reservation import Reservation

# --------------------------------------------------------------
# Classe de test d’intégration complète
# Chaque méthode teste une partie du flux global de données
# --------------------------------------------------------------
class TestFullIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialise le schéma de base de données avant tous les tests
        init_db()

    # ----------------------------------------------------------
    # Test 1 : insertion d’un type de chambre
    # ----------------------------------------------------------
    def test_insert_type_chambre(self):
        with SessionLocal() as s:
            # Création d’un type de chambre pour tests
            tc = TypeChambre(
                nom_type="TestType",
                prix_plancher=50.0,
                prix_plafond="100.0",
                description_chambre="Type test"
            )
            s.add(tc)
            s.commit()
            s.refresh(tc)

            # Vérifie que l’enregistrement a bien été inséré
            row = s.get(TypeChambre, tc.id_type_chambre)
            self.assertIsNotNone(row)
            self.assertEqual(row.nom_type, "TestType")

    # ----------------------------------------------------------
    # Test 2 : insertion d’une chambre associée à un type
    # ----------------------------------------------------------
    def test_insert_chambre_with_type(self):
        with SessionLocal() as s:
            # On récupère un type existant pour lier la chambre
            tc = s.execute(select(TypeChambre)).scalars().first()
            self.assertIsNotNone(tc, "A TypeChambre must exist before adding a Chambre.")

            # Création d’une chambre liée à ce type
            ch = Chambre(
                numero_chambre=999,
                disponible_reservation=True,
                autre_informations="Rez-de-chaussée",
                type_chambre=tc
            )
            s.add(ch)
            s.commit()
            s.refresh(ch)

            # Vérifie la relation entre la chambre et le type
            row = s.get(Chambre, ch.id_chambre)
            self.assertIsNotNone(row)
            self.assertEqual(row.type_chambre.id_type_chambre, tc.id_type_chambre)

    # ----------------------------------------------------------
    # Test 3 : insertion d’un usager
    # ----------------------------------------------------------
    def test_insert_usager(self):
        with SessionLocal() as s:
            # Création d’un usager complet
            u = Usager(
                prenom="Unit",
                nom="Tester",
                adresse="123 rue test",
                mobile="5551234",
                mot_de_passe="password".ljust(60),
                type_usager="Client"
            )
            s.add(u)
            s.commit()
            s.refresh(u)

            # Vérifie que l’usager a bien été inséré
            row = s.get(Usager, u.id_usager)
            self.assertIsNotNone(row)
            self.assertEqual(row.nom, "Tester")

    # ----------------------------------------------------------
    # Test 4 : scénario complet de réservation
    # ----------------------------------------------------------
    def test_insert_reservation_full_flow(self):
        with SessionLocal() as s:
            # Récupère une chambre et un usager existants pour la réservation
            ch = s.execute(select(Chambre)).scalars().first()
            u = s.execute(select(Usager)).scalars().first()

            # Vérifie que les dépendances sont présentes
            self.assertIsNotNone(ch, "Chambre must exist before creating a Reservation.")
            self.assertIsNotNone(u, "Usager must exist before creating a Reservation.")

            # Création d’une réservation complète entre l’usager et la chambre
            r = Reservation(
                date_debut_reservation=datetime.now(),
                date_fin_reservation=datetime.now() + timedelta(days=1),
                prix_jour=75.0,
                info_reservation="Test reservation",
                usager=u,
                chambre=ch
            )
            s.add(r)
            s.commit()
            s.refresh(r)

            # Vérifie que la réservation est bien enregistrée et liée
            row = s.get(Reservation, r.id_reservation)
            self.assertIsNotNone(row)
            self.assertEqual(row.usager.id_usager, u.id_usager)
            self.assertEqual(row.chambre.id_chambre, ch.id_chambre)

# Point d’entrée du test d’intégration
if __name__ == "__main__":
    unittest.main()
