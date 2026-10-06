from django.contrib import admin

from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponibilite', 'proprietaire')
    list_filter = ('type_vehicule', 'disponibilite')
    search_fields = ('immatriculation', 'proprietaire__raison_sociale')