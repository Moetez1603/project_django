from django.urls import path
from .views import home, welcome, list_expeditions, delete_expedition, Expedition_List, Expedition_Detail, Expedition_Delete, ExpeditionCreateView, ExpeditionUpdateView
from .forms import ExpeditionForm

urlpatterns = [
    path('home/', home, name='home'),#route static
    path('welcome/<str:name>/', welcome, name='welcome'),#route parametre
    path('list-expeditions/', list_expeditions, name='list_expeditions'),
    path('details/<int:pk>/', Expedition_Detail.as_view(), name='detail_expedition'),
    path('delete/<int:pk>/', delete_expedition, name='delete_expedition'),
    path('list/', Expedition_List.as_view(), name='expedition_list'),  # class on utilise as_view() pour convertir la classe en vue
    path('expedition/<int:pk>/', Expedition_Detail.as_view(), name='expedition_detail'),
    path('expedition/<int:pk>/delete/', Expedition_Delete.as_view(), name='expedition_delete'),
    path('expedition/create/', ExpeditionCreateView.as_view(), name='expedition_create'),
    path('expedition/<int:pk>/update/', ExpeditionUpdateView.as_view(), name='expedition_update')
]