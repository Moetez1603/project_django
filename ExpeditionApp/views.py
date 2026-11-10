from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Expedition
from django.views.generic import ListView, DetailView,DeleteView,CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import ExpeditionForm

def home(request):
    return HttpResponse("<h1> welcome to ...</h1>")


def welcome(request, name):
    return HttpResponse(f"Hello {name}")


def list_expeditions(request):
    expeditions = Expedition.objects.select_related('entreprise').all()
    return render(request, 'expedition/list.html', {'expeditions': expeditions})


def detail_expedition(request, pk):
    expedition = get_object_or_404(
        Expedition.objects.select_related('entreprise'),
        pk=pk,
    )
    return render(request, 'expedition/detail.html', {'expedition': expedition})


@staff_member_required
@require_POST
def delete_expedition(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    reference = expedition.reference
    expedition.delete()
    messages.success(request, f"L’expédition {reference} a été supprimée.")
    return redirect('list_expeditions')

class Expedition_List(ListView):
    model = Expedition
    template_name = 'expedition/list.html'
    context_object_name = 'Liste'

class Expedition_Detail(DetailView):
    model = Expedition
    template_name = 'expedition/detail.html'
    context_object_name = 'expedition'

class Expedition_Delete(DeleteView):
    model = Expedition
    template_name = 'expedition/confirm_delete.html'
    success_url = reverse_lazy('expedition_list')     # Redirection après la suppression


class ExpeditionCreateView(CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'form.html'
    success_url = reverse_lazy('list_expeditions')

@method_decorator(staff_member_required, name='dispatch')
class ExpeditionUpdateView(UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = 'form.html'
    success_url = reverse_lazy('list_expeditions')