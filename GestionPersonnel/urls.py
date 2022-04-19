from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('consultation', views.consultation, name='consultation'),
    path('ajouterp', views.ajouter, name='ajouter'),
    path('conjoint', views.conjoint, name='conjoint'),
    path('conjoint/personnel', views.conjoint, name='conjoint'),
    path('modifier/<int:id>', views.modifier),
    path('export_pdf', views.printpdf, name='export_pdf'),
    path('export_pdfquiter', views.printpdfquitter, name='export_pdfquiter'),
    path('taboard', views.taboardpersonnel, name='taboard'),

]
