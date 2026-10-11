from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Entreprise, Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations métier', {'fields': ('user_id', 'role', 'telephone')}),
    )
    readonly_fields = ('user_id',)


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal', 'utilisateur__username')
