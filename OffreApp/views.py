from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import OffreForm
from .models import Offre


class OffreListView(ListView):
    model = Offre
    template_name = 'offre/list.html'
    context_object_name = 'offres'
    queryset = Offre.objects.select_related(
        'expedition',
        'transporteur',
        'vehicule',
    )


class OffreDetailView(DetailView):
    model = Offre
    template_name = 'offre/detail.html'
    context_object_name = 'offre'
    queryset = Offre.objects.select_related(
        'expedition',
        'transporteur',
        'vehicule',
    )


class OffreCreateView(CreateView):
    model = Offre
    form_class = OffreForm
    template_name = 'offre/form.html'
    success_url = reverse_lazy('offre_list')


@method_decorator(staff_member_required, name='dispatch')
class OffreUpdateView(UpdateView):
    model = Offre
    form_class = OffreForm
    template_name = 'offre/form.html'
    success_url = reverse_lazy('offre_list')


@method_decorator(staff_member_required, name='dispatch')
class OffreDeleteView(DeleteView):
    model = Offre
    template_name = 'offre/confirm_delete.html'
    success_url = reverse_lazy('offre_list')
