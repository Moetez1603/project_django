from django.contrib import admin

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut', 'date_proposition')
    list_filter = ('statut', 'date_proposition')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale', 'vehicule__immatriculation')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')