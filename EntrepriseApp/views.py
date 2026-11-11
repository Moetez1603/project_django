from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EntrepriseForm
from .models import Entreprise


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = 'entreprise/list.html'
    context_object_name = 'entreprises'
    queryset = Entreprise.objects.select_related('utilisateur')


class EntrepriseDetailView(DetailView):
    model = Entreprise
    template_name = 'entreprise/detail.html'
    context_object_name = 'entreprise'
    queryset = Entreprise.objects.select_related('utilisateur')


class EntrepriseCreateView(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprise/form.html'
    success_url = reverse_lazy('entreprise_list')


@method_decorator(staff_member_required, name='dispatch')
class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = 'entreprise/form.html'
    success_url = reverse_lazy('entreprise_list')


@method_decorator(staff_member_required, name='dispatch')
class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = 'entreprise/confirm_delete.html'
    success_url = reverse_lazy('entreprise_list')
