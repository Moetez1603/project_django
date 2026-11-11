from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule


class VehiculeCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            username='vehicule-admin',
            email='vehicule-admin@example.com',
            password='TestPassword123!',
        )
        cls.transporteur = Entreprise.objects.create(
            raison_sociale='Transporteur Véhicule Test',
            matricule_fiscal='1234567ABM789',
            type_entreprise='transporteur',
            adresse='Adresse transporteur',
            utilisateur=cls.admin_user,
        )
        cls.vehicule = Vehicule.objects.create(
            immatriculation='TEST-VEHICULE-01',
            capacite_kg=1000,
            disponible=True,
            type_vehicule='camionnette',
            entreprise=cls.transporteur,
        )

    def test_vehicle_list_and_detail_pages_render(self):
        response = self.client.get(reverse('vehicule_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ajouter un véhicule')
        self.assertContains(response, self.vehicule.immatriculation)

        response = self.client.get(reverse('vehicule_detail', args=[self.vehicule.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.transporteur.raison_sociale)

    def test_vehicle_can_be_created_from_the_form(self):
        response = self.client.post(reverse('vehicule_create'), {
            'immatriculation': 'TEST-VEHICULE-02',
            'capacite_kg': '1500',
            'disponible': 'on',
            'type_vehicule': 'fourgon',
            'entreprise': self.transporteur.pk,
        })

        self.assertRedirects(response, reverse('vehicule_list'))
        self.assertEqual(Vehicule.objects.count(), 2)

    def test_staff_can_update_and_delete_a_vehicle(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            reverse('vehicule_update', args=[self.vehicule.pk]),
            {
                'immatriculation': self.vehicule.immatriculation,
                'capacite_kg': '1200',
                'disponible': 'on',
                'type_vehicule': 'fourgon',
                'entreprise': self.transporteur.pk,
            },
        )

        self.assertRedirects(response, reverse('vehicule_list'))
        self.vehicule.refresh_from_db()
        self.assertEqual(self.vehicule.capacite_kg, 1200)

        response = self.client.post(reverse('vehicule_delete', args=[self.vehicule.pk]))

        self.assertRedirects(response, reverse('vehicule_list'))
        self.assertFalse(Vehicule.objects.filter(pk=self.vehicule.pk).exists())
