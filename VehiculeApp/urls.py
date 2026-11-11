from django.urls import path

from .views import (
    VehiculeCreateView,
    VehiculeDeleteView,
    VehiculeDetailView,
    VehiculeListView,
    VehiculeUpdateView,
)

urlpatterns = [
    path('list-vehicules/', VehiculeListView.as_view(), name='vehicule_list'),
    path('create/', VehiculeCreateView.as_view(), name='vehicule_create'),
    path('<int:pk>/', VehiculeDetailView.as_view(), name='vehicule_detail'),
    path('<int:pk>/update/', VehiculeUpdateView.as_view(), name='vehicule_update'),
    path('<int:pk>/delete/', VehiculeDeleteView.as_view(), name='vehicule_delete'),
]
