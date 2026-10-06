from django.core.exceptions import ValidationError
from django.db import models

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
        related_name='expeditions_expeditionapp',
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
