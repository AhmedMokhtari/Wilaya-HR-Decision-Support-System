from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('consultation', views.consultation, name='consultation'),
    path('ajouterp', views.ajouter, name='ajouterp'),
    path('conjoint', views.conjoint, name='conjoint'),
    path('modifier/<int:id>', views.modifier),
    path('export_pdf/<int:id>', views.printpdf, name='export_pdf'),
    path('export_pdfquiter/<int:id>', views.printpdfquitter, name='export_pdfquiter'),
    path('taboard', views.taboardpersonnel, name='taboard'),
    path('info/<int:id>', views.info, name='info'),
    path('enfant', views.enfant, name='enfant'),
    path('diplome', views.diplome, name='diplome'),

]
