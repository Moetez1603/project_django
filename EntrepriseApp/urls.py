from django.urls import path

from .views import (
    EntrepriseCreateView,
    EntrepriseDeleteView,
    EntrepriseDetailView,
    EntrepriseListView,
    EntrepriseUpdateView,
)

urlpatterns = [
    path('list-entreprises/', EntrepriseListView.as_view(), name='entreprise_list'),
    path('create/', EntrepriseCreateView.as_view(), name='entreprise_create'),
    path('<int:pk>/', EntrepriseDetailView.as_view(), name='entreprise_detail'),
    path('<int:pk>/update/', EntrepriseUpdateView.as_view(), name='entreprise_update'),
    path('<int:pk>/delete/', EntrepriseDeleteView.as_view(), name='entreprise_delete'),
]
