from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from EntrepriseApp.models import Entreprise


class Expedition(models.Model):
    STATUT_CHOICES = [
        ('publiee', 'Publiée'),
        ('attribuee', 'Attribuée'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    reference = models.CharField(max_length=20, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='publiee')
    chargeur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions_offreapp',
        limit_choices_to={'type_entreprise': 'chargeur'},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reference} : {self.ville_depart} → {self.ville_arrivee}'

    def clean(self):
        super().clean()
        if self.chargeur_id and self.chargeur.type_entreprise != 'chargeur':
            raise ValidationError({
                'chargeur': 'Une expédition doit être liée à un chargeur.'
            })

    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%Y')
        prefixe = f'EXP_{annee}_'

        dernier = cls.objects.filter(reference__startswith=prefixe).order_by('reference').last()
        compteur = int(dernier.reference[-5:]) + 1 if dernier else 1

        if compteur > 99999:
            raise ValueError('Limite maximale atteinte.')

        return f'{prefixe}{compteur:05d}'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()

        self.full_clean()
        super().save(*args, **kwargs)
