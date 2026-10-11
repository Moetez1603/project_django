from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from EntrepriseApp.models import Entreprise


class Vehicule(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('camionnette', 'Camionnette'),
        ('fourgon', 'Fourgon'),
        ('camion porteur', 'Camion porteur'),
        ('semi-remorque', 'Semi-remorque'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    capacite_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(100, 'Capacité doit être supérieure à 100 kg.')]
    )
    disponible = models.BooleanField(default=True)
    type_vehicule = models.CharField(
        max_length=50,
        choices=TYPE_VEHICULE_CHOICES,
        default='camionnette',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='vehicules',
        limit_choices_to={'type_entreprise': 'transporteur'},
    )

    def __str__(self):
        return f'{self.get_type_vehicule_display()} ({self.immatriculation})'

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({
                'entreprise': 'Un véhicule doit appartenir à une entreprise de type transporteur.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
