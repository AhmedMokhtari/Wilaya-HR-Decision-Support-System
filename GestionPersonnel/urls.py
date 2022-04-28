from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('consultation', views.consultation, name='consultation'),
    path('ajouterp', views.ajouter, name='ajouterp'),
    path('ajouter_conjoint', views.conjoint, name='ajouter_conjoint'),
    path('modifier/<int:id>', views.modifier,name="modifier"),
    path('export_pdf/<int:id>', views.printpdf, name='export_pdf'),
    path('export_pdfquiter/<int:id>', views.printpdfquitter, name='export_pdfquiter'),
    path('taboard', views.taboardpersonnel, name='taboard'),
    path('info/<int:id>', views.info, name='info'),
    path('ajouter_enfant', views.enfant, name='ajouter_enfant'),
    path('ajouter_diplome', views.diplome, name='ajouter_diplome'),
    path(r'^export/xls/$', views.export_perso_csv, name='export_perso_xls'),
]
