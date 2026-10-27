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

    def test_admin_can_create_an_expedition_and_generate_its_reference(self):
        self.client.force_login(self.admin_user)

        response = self.client.post('/admin/ExpeditionApp/expedition/add/', {
            'ville_depart': 'Sousse',
            'ville_arrivee': 'Monastir',
            'description': 'Test de création',
            'poids_kg': '75.50',
            'date_souhaitee': '2026-11-15',
            'statut': 'publiee',
            'entreprise': str(self.company.pk),
            'offres-TOTAL_FORMS': '0',
            'offres-INITIAL_FORMS': '0',
            'offres-MIN_NUM_FORMS': '0',
            'offres-MAX_NUM_FORMS': '1000',
            '_save': 'Enregistrer',
        })

        self.assertEqual(response.status_code, 302)
        expedition = Expedition.objects.get(ville_depart='Sousse')
        self.assertEqual(expedition.ville_arrivee, 'Monastir')
        self.assertEqual(expedition.poids_kg, 75.50)
        self.assertTrue(expedition.reference.startswith('EXP_'))

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

    def test_expedition_list_page_displays_saved_expeditions(self):
        response = self.client.get('/expedition/list-expeditions/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expedition/list.html')
        self.assertContains(response, self.expeditions[0].reference)
        self.assertContains(response, 'Tunis')
        self.assertContains(response, 'Sfax')
        self.assertContains(response, 'Chargeur Test')
        self.assertContains(
            response,
            f'<a href="/details/{self.expeditions[0].pk}/">{self.expeditions[0].reference}</a>',
            html=True,
        )

    def test_expedition_list_shows_delete_button_only_to_staff(self):
        response = self.client.get('/expedition/list-expeditions/')
        self.assertNotContains(response, 'Supprimer')

        self.client.force_login(self.admin_user)
        response = self.client.get('/expedition/list-expeditions/')
        self.assertContains(response, 'Supprimer')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_staff_can_delete_expedition_from_list(self):
        expedition = self.expeditions[0]
        self.client.force_login(self.admin_user)

        response = self.client.post(f'/expedition/delete/{expedition.pk}/', follow=True)

        self.assertRedirects(response, '/expedition/list-expeditions/')
        self.assertFalse(Expedition.objects.filter(pk=expedition.pk).exists())
        self.assertContains(response, f"L’expédition {expedition.reference} a été supprimée.")

    def test_get_request_cannot_delete_expedition(self):
        expedition = self.expeditions[0]
        self.client.force_login(self.admin_user)

        response = self.client.get(f'/expedition/delete/{expedition.pk}/')

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Expedition.objects.filter(pk=expedition.pk).exists())

    def test_non_staff_cannot_delete_expedition(self):
        expedition = self.expeditions[0]
        self.client.logout()

        response = self.client.post(f'/expedition/delete/{expedition.pk}/')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expedition.objects.filter(pk=expedition.pk).exists())

    def test_expedition_details_page_displays_saved_expedition(self):
        expedition = self.expeditions[0]

        response = self.client.get(f'/details/{expedition.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expedition/detail.html')
        self.assertContains(response, expedition.reference)
        self.assertContains(response, 'Tunis')
        self.assertContains(response, 'Sfax')

    def test_expedition_details_page_is_also_available_under_expedition_prefix(self):
        expedition = self.expeditions[0]

        response = self.client.get(f'/expedition/details/{expedition.pk}/')

        self.assertEqual(response.status_code, 200)

    def test_expedition_details_page_returns_404_for_unknown_id(self):
        response = self.client.get('/details/999999/')

        self.assertEqual(response.status_code, 404)


class ExpeditionUrlTests(TestCase):
    def test_welcome_page_displays_the_name_from_the_url(self):
        response = self.client.get('/expedition/welcome/Moetez/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello Moetez')
