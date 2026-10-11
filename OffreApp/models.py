from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from EntrepriseApp.models import Entreprise
from ExpeditionApp.models import Expedition
from VehiculeApp.models import Vehicule


class Offre(models.Model):
    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee',
    )
    date_proposition = models.DateField(auto_now_add=True)
    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='offres',
    )
    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres',
        limit_choices_to={'type_entreprise': 'transporteur'},
    )
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='offres',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Offre #{self.pk} sur {self.expedition.reference} ({self.prix} DT)'

    def clean(self):
        super().clean()
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError({
                'transporteur': 'Une offre doit être émise par une entreprise de type transporteur.'
            })
        if self.vehicule_id and self.transporteur_id:
            if self.vehicule.entreprise_id != self.transporteur_id:
                raise ValidationError({
                    'vehicule': 'Le véhicule sélectionné doit appartenir au transporteur.'
                })
        if self.vehicule_id and not self.vehicule.disponible:
            raise ValidationError({
                'vehicule': 'Le véhicule sélectionné doit être disponible.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)