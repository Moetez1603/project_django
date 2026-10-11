from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
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

    reference = models.CharField(max_length=20, unique=True, blank=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='publiee')
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions',
        limit_choices_to={'type_entreprise': 'chargeur'},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reference} : {self.ville_depart} → {self.ville_arrivee}'

    @classmethod
    def generate_reference(cls):
        annee = timezone.now().strftime('%Y')
        prefixe = f'EXP_{annee}_'
        dernier = cls.objects.filter(reference__startswith=prefixe).order_by('reference').last()
        if dernier and dernier.reference[-5:].isdigit():
            compteur = int(dernier.reference[-5:]) + 1
        else:
            compteur = 1
        return f'{prefixe}{compteur:05d}'

    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({
                'entreprise': 'Une expédition doit être liée à une entreprise de type chargeur.'
            })

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        self.full_clean()
        super().save(*args, **kwargs)
