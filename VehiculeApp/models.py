from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.
class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=11, unique=True)
    capacite_kg = models.IntegerField()
    disponibilite = models.BooleanField(default=True)

    type_vehicule = models.CharField(max_length=50, choices=[
    ('camionnette', 'Camionnette'),
    ('fourgon', 'Fourgon'),
    ('camion porteur', 'Camion porteur'),
    ('semi remorque', 'Semi remorque')
], default='camionnette')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proprietaire = models.ForeignKey(Entreprise,
     on_delete=models.CASCADE,
      related_name='vehicules'
      )

    def __str__(self):
        return f"{self.type_vehicule} ({self.immatriculation})"
