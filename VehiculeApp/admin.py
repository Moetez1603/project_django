from django.contrib import admin

from .models import Vehicule


class VehiculeAdmin(admin.ModelAdmin):
	list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
	list_filter = ('type_vehicule', 'disponible', 'entreprise')
	search_fields = ('immatriculation', 'entreprise__raison_sociale')
	list_editable = ('disponible',)
	ordering = ('immatriculation',)
	readonly_fields = ('created_at', 'updated_at')
	fieldsets = (
		('Informations du véhicule', {
			'fields': ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible')
		}),
		('Entreprise', {
			'fields': ('entreprise',)
		}),
		('Dates', {
			'fields': ('created_at', 'updated_at')
		}),
	)


admin.site.register(Vehicule, VehiculeAdmin)
