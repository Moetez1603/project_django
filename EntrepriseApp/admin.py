from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Entreprise, Utilisateur
from VehiculeApp.models import Vehicule


class UtilisateurCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ('username', 'email', 'role', 'telephone')


class UtilisateurAdmin(UserAdmin):
    add_form = UtilisateurCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'telephone', 'password1', 'password2'),
        }),
    )
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    readonly_fields = ('user_id', 'last_login', 'date_joined', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user_id', 'username', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'telephone', 'role')
        }),
        ('Autorisations', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )


class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'created_at')
    readonly_fields = ('created_at',)
    extra = 1
    show_change_link = True


class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal', 'utilisateur__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (VehiculeInline,)

    def get_inline_instances(self, request, obj=None):
        if obj is None or obj.type_entreprise != 'transporteur':
            return []
        return super().get_inline_instances(request, obj)

    fieldsets = (
        ('Identification', {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise')
        }),
        ('Coordonnées et compte', {
            'fields': ('adresse', 'utilisateur')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Entreprise, EntrepriseAdmin)
