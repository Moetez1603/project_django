from django.test import TestCase

# Create your tests here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from EntrepriseApp.models import Entreprise
from ExpeditionApp.models import Expedition
from OffreApp.models import Offre
from VehiculeApp.models import Vehicule


@override_settings(ALLOWED_HOSTS=['testserver'])
class OffreAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username='offre-admin',
            email='offre-admin@example.com',
            password='TestPassword123!',
        )
        cls.chargeur = Entreprise.objects.create(
            raison_sociale='Chargeur Test Offre',
            matricule_fiscal='1234567ABM123',
            type_entreprise='chargeur',
            adresse='Adresse chargeur',
            utilisateur=cls.admin_user,
        )
        cls.transporteur_user = get_user_model().objects.create_user(
            username='transporteur-test',
            email='transporteur-test@example.com',
            password='TestPassword123!',
            role='transporteur',
        )
        cls.transporteur = Entreprise.objects.create(
            raison_sociale='Transporteur Test',
            matricule_fiscal='7654321ABM456',
            type_entreprise='transporteur',
            adresse='Adresse transporteur',
            utilisateur=cls.transporteur_user,
        )
        cls.expedition = Expedition.objects.create(
            ville_depart='Tunis',
            ville_arrivee='Sfax',
            poids_kg='100.00',
            date_souhaitee='2026-11-01',
            entreprise=cls.chargeur,
        )
        cls.vehicule = Vehicule.objects.create(
            immatriculation='TEST-ADMIN-01',
            capacite_kg=1000,
            disponible=True,
            type_vehicule='camionnette',
            entreprise=cls.transporteur,
        )
        cls.offre = Offre.objects.create(
            prix='150.00',
            delai_jours=2,
            expedition=cls.expedition,
            transporteur=cls.transporteur,
            vehicule=cls.vehicule,
        )

    def test_accepted_offer_price_and_delay_are_read_only(self):
        model_admin = admin.site._registry[Offre]
        self.offre.statut = 'acceptee'

        readonly_fields = model_admin.get_readonly_fields(None, self.offre)

        self.assertIn('prix', readonly_fields)
        self.assertIn('delai_jours', readonly_fields)

    def test_export_action_returns_selected_offers_as_csv(self):
        self.client.force_login(self.admin_user)

        response = self.client.post('/admin/OffreApp/offre/', {
            'action': 'exporter_offres_csv',
            'index': '0',
            'select_across': '0',
            '_selected_action': str(self.offre.pk),
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn(self.expedition.reference, response.content.decode())
        self.assertIn(self.transporteur.raison_sociale, response.content.decode())

    def test_offer_status_is_rendered_as_a_badge(self):
        self.client.force_login(self.admin_user)

        response = self.client.get('/admin/OffreApp/offre/')

        self.assertContains(response, 'status-badge--offre-proposee')
        self.assertContains(response, 'Proposée')
