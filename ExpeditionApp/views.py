from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Expedition

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
