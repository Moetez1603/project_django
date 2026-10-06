from django.contrib import admin

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('expedition', 'transporteur', 'prix', 'delai_jours', 'statut', 'created_at')
    list_filter = ('statut', 'expedition__statut')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale')