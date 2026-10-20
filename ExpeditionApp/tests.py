from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import override_settings

from EntrepriseApp.models import Entreprise
from ExpeditionApp.models import Expedition
from django.contrib import admin


@override_settings(ALLOWED_HOSTS=['testserver'])
class IntegrityDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username='dashboard-admin',
            email='dashboard-admin@example.com',
            password='TestPassword123!',
        )

    def test_dashboard_is_available_to_admin_and_shows_all_checks(self):
        self.client.force_login(self.admin_user)

        response = self.client.get('/admin/health-check/')

        self.assertEqual(response.status_code, 200)
        for title in (
            'Offres orphelines',
            'Expéditions publiées depuis plus de 7 jours',
            'Transporteurs sans flotte',
            'Véhicules disponibles déjà attribués',
            'Propositions en doublon',
        ):
            self.assertContains(response, title)

    def test_dashboard_requires_admin_access(self):
        response = self.client.get('/admin/health-check/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_admin_index_links_to_dashboard(self):
        self.client.force_login(self.admin_user)

        response = self.client.get('/admin/')

        self.assertContains(response, '/admin/health-check/')

    def test_dashboard_exports_findings_as_csv(self):
        self.client.force_login(self.admin_user)

        response = self.client.get('/admin/health-check/?format=csv')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('controle,element,detail,url', response.content.decode())


@override_settings(ALLOWED_HOSTS=['testserver'])
class ExpeditionAdminActionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username='expedition-admin',
            email='expedition-admin@example.com',
            password='TestPassword123!',
        )
        cls.company = Entreprise.objects.create(
            raison_sociale='Chargeur Test',
            matricule_fiscal='1234567ABM123',
            type_entreprise='chargeur',
            adresse='Adresse de test',
            utilisateur=cls.admin_user,
        )
        cls.expeditions = [
            Expedition.objects.create(
                ville_depart='Tunis',
                ville_arrivee='Sfax',
                poids_kg='100.00',
                date_souhaitee='2026-11-01',
                entreprise=cls.company,
            )
            for _ in range(2)
        ]

    def test_cloturer_action_marks_selected_expeditions_as_delivered(self):
        self.client.force_login(self.admin_user)

        response = self.client.post('/admin/ExpeditionApp/expedition/', {
            'action': 'cloturer_expeditions',
            'index': '0',
            'select_across': '0',
            '_selected_action': [str(expedition.pk) for expedition in self.expeditions],
        })

        self.assertEqual(response.status_code, 302)
        for expedition in self.expeditions:
            expedition.refresh_from_db()
            self.assertEqual(expedition.statut, 'livree')

    def test_status_is_rendered_as_a_badge_not_an_editable_input(self):
        self.client.force_login(self.admin_user)

        response = self.client.get('/admin/ExpeditionApp/expedition/')
        model_admin = admin.site._registry[Expedition]

        self.assertContains(response, 'status-badge--expedition-publiee')
        self.assertNotIn('statut', model_admin.list_editable)

    def test_close_action_is_registered(self):
        model_admin = admin.site._registry[Expedition]

        self.assertIn('cloturer_expeditions', model_admin.actions)
