from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('consultation',views.consultation,name = 'consultation'),
    path('ajouter',views.ajouter_aff,name = 'ajouter'),
]
