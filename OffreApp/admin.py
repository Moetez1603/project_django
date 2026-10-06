from django.contrib import admin

from .models import Expedition


@admin.register(Expedition)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('reference', 'chargeur', 'ville_depart', 'ville_arrivee', 'statut', 'created_at')
    list_filter = ('statut',)
    search_fields = ('reference', 'chargeur__raison_sociale', 'ville_depart', 'ville_arrivee')