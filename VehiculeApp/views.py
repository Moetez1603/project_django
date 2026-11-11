from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import VehiculeForm
from .models import Vehicule


class VehiculeListView(ListView):
    model = Vehicule
    template_name = 'vehicule/list.html'
    context_object_name = 'vehicules'
    queryset = Vehicule.objects.select_related('entreprise')


class VehiculeDetailView(DetailView):
    model = Vehicule
    template_name = 'vehicule/detail.html'
    context_object_name = 'vehicule'
    queryset = Vehicule.objects.select_related('entreprise')


class VehiculeCreateView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = 'vehicule/form.html'
    success_url = reverse_lazy('vehicule_list')


@method_decorator(staff_member_required, name='dispatch')
class VehiculeUpdateView(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = 'vehicule/form.html'
    success_url = reverse_lazy('vehicule_list')


@method_decorator(staff_member_required, name='dispatch')
class VehiculeDeleteView(DeleteView):
    model = Vehicule
    template_name = 'vehicule/confirm_delete.html'
    success_url = reverse_lazy('vehicule_list')
