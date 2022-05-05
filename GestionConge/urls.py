from django.urls import path
from . import views

urlpatterns = [
    path('ajouterconge', views.conge, name='ajouterconje'),
    path('deleteconge/<int:id>', views.delete, name='deleteconge'),
]
