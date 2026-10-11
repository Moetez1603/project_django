from django.contrib import admin

from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'entreprise', 'ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'statut')
    list_filter = ('statut', 'date_souhaitee')
    search_fields = ('reference', 'entreprise__raison_sociale', 'ville_depart', 'ville_arrivee')
    readonly_fields = ('reference',)
