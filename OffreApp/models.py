from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from EntrepriseApp.models import Entreprise


class Offre(models.Model):
    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition',
        on_delete=models.CASCADE,
        related_name='offres',
    )
    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres_transporteur',
        limit_choices_to={'type_entreprise': 'transporteur'},
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    delai_jours = models.IntegerField(validators=[MinValueValidator(1)])
    statut = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Offre {self.pk} – {self.expedition.reference}'

    def clean(self):
        super().clean()
        if self.transporteur_id and self.transporteur.type_entreprise != 'transporteur':
            raise ValidationError({
                'transporteur': 'Une offre doit être attribuée à un transporteur.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)