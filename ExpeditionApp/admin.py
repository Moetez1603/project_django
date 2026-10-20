from django.contrib import messages
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.utils.html import format_html
from django.utils import timezone

from OffreApp.models import Offre
from .models import Expedition

admin.site.site_header = "TransConnect - Administration"
admin.site.site_title = "TransConnect"
admin.site.index_title = "Tableau de bord"


class EnRetardFilter(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == "oui":
            return queryset.filter(
                statut="publiee",
                date_souhaitee__lt=aujourd_hui,
            )
        if self.value() == "non":
            return queryset.exclude(
                statut="publiee",
                date_souhaitee__lt=aujourd_hui,
            )
        return queryset


class ExpeditionActionForm(ActionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].label = "Action"


class OffreInline(admin.StackedInline):
    model = Offre
    extra = 0
    fk_name = 'expedition'
    readonly_fields = ('transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    show_change_link = True
    can_delete = False


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'ville_depart',
        'ville_arrivee',
        'poids_kg',
        'date_souhaitee',
        'statut_badge',
        'entreprise',
    )
    list_filter = ('statut', 'date_souhaitee', 'entreprise', EnRetardFilter)
    search_fields = (
        'reference',
        'ville_depart',
        'ville_arrivee',
        'entreprise__raison_sociale',
    )
    ordering = ('-date_souhaitee',)
    list_per_page = 20
    date_hierarchy = 'date_souhaitee'
    readonly_fields = ('reference', 'created_at', 'updated_at')
    autocomplete_fields = ('entreprise',)
    inlines = (OffreInline,)
    action_form = ExpeditionActionForm
    actions = (
        'cloturer_expeditions',
        'set_status_publiee',
        'set_status_attribuee',
        'set_status_en_cours',
        'set_status_livree',
        'set_status_annulee',
        'delete_selected',
    )
    fieldsets = (
        ('Itinéraire', {
            'fields': ('ville_depart', 'ville_arrivee', 'description')
        }),
        ('Détails de l’expédition', {
            'fields': ('reference', 'poids_kg', 'date_souhaitee')
        }),
        ('Suivi', {
            'fields': ('statut', 'entreprise')
        }),
        ('Dates système', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description="Statut", ordering='statut')
    def statut_badge(self, expedition):
        badge_classes = {
            'publiee': 'publiee',
            'attribuee': 'attribuee',
            'en_cours': 'en-cours',
            'livree': 'livree',
            'annulee': 'annulee',
        }
        return format_html(
            '<span class="status-badge status-badge--expedition-{}">{}</span>',
            badge_classes.get(expedition.statut, 'inconnu'),
            expedition.get_statut_display(),
        )

    def _set_status(self, request, queryset, statut, success_message):
        selected_count = queryset.count()
        for expedition in queryset.iterator():
            expedition.statut = statut
            expedition.save(update_fields=('statut', 'updated_at'))

        self.message_user(
            request,
            success_message.format(count=selected_count),
            level=messages.SUCCESS,
        )

    @admin.action(description="Clôturer les expéditions sélectionnées (statut : Livrée)")
    def cloturer_expeditions(self, request, queryset):
        self._set_status(
            request,
            queryset,
            'livree',
            "{count} expédition(s) clôturée(s) comme livrée(s).",
        )

    @admin.action(description="Passer au statut : Publiée")
    def set_status_publiee(self, request, queryset):
        self._set_status(request, queryset, 'publiee', "{count} expédition(s) passée(s) au statut Publiée.")

    @admin.action(description="Passer au statut : Attribuée")
    def set_status_attribuee(self, request, queryset):
        self._set_status(request, queryset, 'attribuee', "{count} expédition(s) passée(s) au statut Attribuée.")

    @admin.action(description="Passer au statut : En cours")
    def set_status_en_cours(self, request, queryset):
        self._set_status(request, queryset, 'en_cours', "{count} expédition(s) passée(s) au statut En cours.")

    @admin.action(description="Passer au statut : Livrée")
    def set_status_livree(self, request, queryset):
        self._set_status(request, queryset, 'livree', "{count} expédition(s) passée(s) au statut Livrée.")

    @admin.action(description="Passer au statut : Annulée")
    def set_status_annulee(self, request, queryset):
        self._set_status(request, queryset, 'annulee', "{count} expédition(s) passée(s) au statut Annulée.")
