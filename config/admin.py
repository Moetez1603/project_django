import csv
from datetime import timedelta
from urllib.parse import urlencode

from django.contrib.admin import AdminSite
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone


class TransConnectAdminSite(AdminSite):
    def get_urls(self):
        custom_urls = [
            path(
                'health-check/',
                self.admin_view(self.health_check_view),
                name='health_check',
            ),
        ]
        return custom_urls + super().get_urls()

    def health_check_view(self, request):
        from EntrepriseApp.models import Entreprise
        from ExpeditionApp.models import Expedition
        from OffreApp.models import Offre
        from VehiculeApp.models import Vehicule

        checks = []

        def add_check(title, rule, entries):
            checks.append({
                'title': title,
                'rule': rule,
                'entries': entries,
                'count': len(entries),
            })

        orphan_offers = Offre.objects.filter(
            statut__in=('proposee', 'acceptee'),
        ).exclude(
            expedition__statut__in=('publiee', 'attribuee'),
        ).select_related('expedition', 'transporteur')
        add_check(
            'Offres orphelines',
            'Une offre proposée ou acceptée doit concerner une expédition publiée ou attribuée.',
            [
                {
                    'label': str(offer),
                    'detail': f'Expédition {offer.expedition.reference} — {offer.get_statut_display()}',
                    'url': reverse('admin:OffreApp_offre_change', args=(offer.pk,)),
                }
                for offer in orphan_offers
            ],
        )

        old_publications = Expedition.objects.filter(
            statut='publiee',
            created_at__lt=timezone.now() - timedelta(days=7),
        )
        add_check(
            'Expéditions publiées depuis plus de 7 jours',
            'Repère les expéditions publiées dont la date de création remonte à plus de sept jours.',
            [
                {
                    'label': str(expedition),
                    'detail': f'Créée le {timezone.localtime(expedition.created_at):%d/%m/%Y}',
                    'url': reverse('admin:ExpeditionApp_expedition_change', args=(expedition.pk,)),
                }
                for expedition in old_publications
            ],
        )

        transporters_without_vehicles = Entreprise.objects.filter(
            type_entreprise='transporteur',
        ).annotate(
            vehicle_count=Count('vehicules'),
        ).filter(
            vehicle_count=0,
        )
        add_check(
            'Transporteurs sans flotte',
            'Repère les entreprises de transport qui ne possèdent aucun véhicule.',
            [
                {
                    'label': company.raison_sociale,
                    'detail': 'Aucun véhicule associé',
                    'url': reverse('admin:EntrepriseApp_entreprise_change', args=(company.pk,)),
                }
                for company in transporters_without_vehicles
            ],
        )

        available_vehicles_with_accepted_offers = Vehicule.objects.filter(
            disponible=True,
            offres__statut='acceptee',
        ).select_related('entreprise').distinct()
        add_check(
            'Véhicules disponibles déjà attribués',
            'Un véhicule lié à une offre acceptée ne devrait plus être marqué disponible.',
            [
                {
                    'label': str(vehicle),
                    'detail': f'Transporteur : {vehicle.entreprise.raison_sociale}',
                    'url': reverse('admin:VehiculeApp_vehicule_change', args=(vehicle.pk,)),
                }
                for vehicle in available_vehicles_with_accepted_offers
            ],
        )

        duplicate_proposals = Offre.objects.filter(
            statut='proposee',
        ).values(
            'expedition_id',
            'expedition__reference',
            'transporteur_id',
            'transporteur__raison_sociale',
        ).annotate(
            proposal_count=Count('pk'),
        ).filter(
            proposal_count__gt=1,
        ).order_by(
            'expedition__reference',
            'transporteur__raison_sociale',
        )
        add_check(
            'Propositions en doublon',
            'Un transporteur ne devrait pas avoir plusieurs offres proposées pour la même expédition.',
            [
                {
                    'label': f"{group['expedition__reference']} — {group['transporteur__raison_sociale']}",
                    'detail': f"{group['proposal_count']} offres proposées",
                    'url': (
                        reverse('admin:OffreApp_offre_changelist')
                        + '?'
                        + urlencode({
                            'expedition__id__exact': group['expedition_id'],
                            'transporteur__id__exact': group['transporteur_id'],
                            'statut__exact': 'proposee',
                        })
                    ),
                }
                for group in duplicate_proposals
            ],
        )

        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="controle-integrite.csv"'
            writer = csv.writer(response)
            writer.writerow(('controle', 'element', 'detail', 'url'))
            for check in checks:
                for entry in check['entries']:
                    writer.writerow((
                        check['title'],
                        entry['label'],
                        entry['detail'],
                        request.build_absolute_uri(entry['url']),
                    ))
            return response

        return render(
            request,
            'admin/health_check.html',
            {
                **self.each_context(request),
                'title': 'Contrôle d’intégrité',
                'checks': checks,
                'total_anomalies': sum(check['count'] for check in checks),
            },
        )
