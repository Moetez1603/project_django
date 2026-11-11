from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from EntrepriseApp.models import Entreprise


class EntrepriseCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.admin_user = user_model.objects.create_superuser(
            username='entreprise-admin',
            email='entreprise-admin@example.com',
            password='TestPassword123!',
        )
        cls.entreprise = Entreprise.objects.create(
            raison_sociale='Entreprise Test',
            matricule_fiscal='1234567ABM123',
            type_entreprise='chargeur',
            adresse='Adresse test',
            utilisateur=cls.admin_user,
        )
        cls.second_user = user_model.objects.create_user(
            username='entreprise-second-user',
            email='entreprise-second@example.com',
            password='TestPassword123!',
            role='transporteur',
        )

    def test_enterprise_list_and_detail_pages_render(self):
        response = self.client.get(reverse('entreprise_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter une entreprise')
        self.assertContains(response, self.entreprise.raison_sociale)

        response = self.client.get(
            reverse('entreprise_detail', args=[self.entreprise.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.admin_user.username)

    def test_enterprise_can_be_created_from_the_form(self):
        response = self.client.post(reverse('entreprise_create'), {
            'raison_sociale': 'Nouvelle entreprise',
            'matricule_fiscal': '7654321ABM456',
            'type_entreprise': 'transporteur',
            'adresse': 'Nouvelle adresse',
            'utilisateur': self.second_user.pk,
        })

        self.assertRedirects(response, reverse('entreprise_list'))
        self.assertTrue(
            Entreprise.objects.filter(raison_sociale='Nouvelle entreprise').exists()
        )

    def test_staff_can_update_and_delete_an_enterprise(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse('entreprise_update', args=[self.entreprise.pk]),
            {
                'raison_sociale': 'Entreprise modifiée',
                'matricule_fiscal': self.entreprise.matricule_fiscal,
                'type_entreprise': 'chargeur',
                'adresse': 'Adresse modifiée',
                'utilisateur': self.admin_user.pk,
            },
        )

        self.assertRedirects(response, reverse('entreprise_list'))
        self.entreprise.refresh_from_db()
        self.assertEqual(self.entreprise.raison_sociale, 'Entreprise modifiée')

        response = self.client.post(
            reverse('entreprise_delete', args=[self.entreprise.pk])
        )

        self.assertRedirects(response, reverse('entreprise_list'))
        self.assertFalse(Entreprise.objects.filter(pk=self.entreprise.pk).exists())

    def test_non_staff_cannot_update_or_delete_an_enterprise(self):
        self.client.force_login(self.second_user)

        update_response = self.client.get(
            reverse('entreprise_update', args=[self.entreprise.pk])
        )
        delete_response = self.client.get(
            reverse('entreprise_delete', args=[self.entreprise.pk])
        )

        self.assertEqual(update_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)
        self.assertTrue(Entreprise.objects.filter(pk=self.entreprise.pk).exists())
