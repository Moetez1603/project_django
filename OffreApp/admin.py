import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html

from .models import Offre


class OffreAdmin(admin.ModelAdmin):
	list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut_badge', 'date_proposition')
	list_filter = ('statut', 'date_proposition', 'transporteur', 'expedition')
	search_fields = ('expedition__reference', 'transporteur__raison_sociale', 'vehicule__immatriculation')
	ordering = ('-date_proposition',)
	readonly_fields = ('date_proposition', 'created_at', 'updated_at')
	actions = ('exporter_offres_csv', 'delete_selected')
	fieldsets = (
		('Expédition et transporteur', {
			'fields': ('expedition', 'transporteur', 'vehicule')
		}),
		('Conditions de l’offre', {
			'fields': ('prix', 'delai_jours', 'statut')
		}),
		('Dates', {
			'fields': ('date_proposition', 'created_at', 'updated_at'),
			'classes': ('collapse',),
		}),
	)

	def get_readonly_fields(self, request, obj=None):
		readonly_fields = list(super().get_readonly_fields(request, obj))
		if obj and obj.statut == 'acceptee':
			readonly_fields.extend(('prix', 'delai_jours'))
		return readonly_fields

	@admin.display(description="Statut", ordering='statut')
	def statut_badge(self, offre):
		badge_classes = {
			'proposee': 'proposee',
			'acceptee': 'acceptee',
			'refusee': 'refusee',
			'retiree': 'retiree',
		}
		return format_html(
			'<span class="status-badge status-badge--offre-{}">{}</span>',
			badge_classes.get(offre.statut, 'inconnu'),
			offre.get_statut_display(),
		)

	@admin.action(description="Exporter la sélection en CSV")
	def exporter_offres_csv(self, request, queryset):
		response = HttpResponse(content_type='text/csv; charset=utf-8')
		response['Content-Disposition'] = 'attachment; filename="offres.csv"'
		writer = csv.writer(response)
		writer.writerow(('reference_expedition', 'transporteur', 'prix', 'statut'))
		for offre in queryset.select_related('expedition', 'transporteur'):
			writer.writerow((
				offre.expedition.reference,
				offre.transporteur.raison_sociale,
				offre.prix,
				offre.get_statut_display(),
			))
		return response

admin.site.register(Offre, OffreAdmin)
