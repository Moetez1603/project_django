from django.urls import path
from .views import delete_expedition, detail_expedition, home, list_expeditions, welcome

urlpatterns = [
    path('home/', home, name='home'),#route static
    path('welcome/<str:name>/', welcome, name='welcome'),#route parametre
    path('list-expeditions/', list_expeditions, name='list_expeditions'),
    path('details/<int:pk>/', detail_expedition, name='detail_expedition'),
    path('delete/<int:pk>/', delete_expedition, name='delete_expedition'),
]