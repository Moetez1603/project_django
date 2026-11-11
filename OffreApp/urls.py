from django.urls import path

from .views import (
    OffreCreateView,
    OffreDeleteView,
    OffreDetailView,
    OffreListView,
    OffreUpdateView,
)

urlpatterns = [
    path('list-offres/', OffreListView.as_view(), name='offre_list'),
    path('create/', OffreCreateView.as_view(), name='offre_create'),
    path('<int:pk>/', OffreDetailView.as_view(), name='offre_detail'),
    path('<int:pk>/update/', OffreUpdateView.as_view(), name='offre_update'),
    path('<int:pk>/delete/', OffreDeleteView.as_view(), name='offre_delete'),
]
