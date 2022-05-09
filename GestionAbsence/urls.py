from django.urls import path
from . import views

urlpatterns = [
    path('taboardab', views.taboardabsence, name='taboardab'),
    path('absence', views.absence, name='absence'),
    path('ajouterab', views.ajouterabsence, name='ajouterab'),
    path('export/abs/', views.export_abs_csv, name='export_abs_xls'),
    path('modifierabs/<int:id>', views.modifierabs, name="modifierabs"),
    path('modifierabsence/<int:id>', views.modifierabsence, name="modifierabsence"),
]