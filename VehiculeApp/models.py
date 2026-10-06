from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from EntrepriseApp.models import Entreprise


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=11, unique=True)
    capacite_kg = models.IntegerField(
        validators=[MinValueValidator(100, 'Capacité doit être supérieure à 100 kg.')]
    )
    disponibilite = models.BooleanField(default=True)
    type_vehicule = models.CharField(
        max_length=50,
        choices=[
            ('camionnette', 'Camionnette'),
            ('fourgon', 'Fourgon'),
            ('camion porteur', 'Camion porteur'),
            ('semi remorque', 'Semi remorque'),
        ],
        default='camionnette',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proprietaire = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules',
    )

    def __str__(self):
        return f'{self.type_vehicule} ({self.immatriculation})'

    def clean(self):
        super().clean()
        if self.proprietaire_id and self.proprietaire.type_entreprise != 'transporteur':
            raise ValidationError({
                'proprietaire': 'Un véhicule doit appartenir à un transporteur.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
