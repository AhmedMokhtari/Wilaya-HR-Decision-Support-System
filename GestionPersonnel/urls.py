from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('consultation', views.consultation, name='consultation'),
    path('persoinfo', views.persoinfoimg, name='persoinfo'),
    path('perso-json/<str:obj>/', views.get_json_perso_data, name='perso-json'),
    path('ajouterp', views.ajouter, name='ajouterp'),
    path('ajouter_conjoint', views.ajouter_conjoint, name='ajouter_conjoint'),
    path('modifier_conjoint/<int:id>', views.modifier_conjoint, name='modifier_conjoint'),
    path('modifier/<int:id>', views.modifier,name="modifier"),
    path('export_pdf/<int:id>', views.printpdf, name='export_pdf'),
    path('export_pdfquiter/<int:id>', views.printpdfquitter, name='export_pdfquiter'),
    path('taboard', views.taboardpersonnel, name='taboard'),
    path('info/<int:id>', views.info, name='info'),
    path('ajouter_enfant', views.ajouter_enfant, name='ajouter_enfant'),
    path('modifier_enfant/<int:id>', views.modifier_enfant, name='modifier_enfant'),
    path('ajouter_diplome', views.ajouter_diplome, name='ajouter_diplome'),
    path('modifier_diplome/<int:id>', views.modifer_diplome, name='modifier_diplome'),
    path('ajaxtaboardpersonnel', views.ajaxtaboardpersonnel, name='ajaxtaboardpersonnel'),
    path('ajaxajouterloadgrade', views.ajaxajouterloadgrade, name='ajaxajouterloadgrade'),
    path('export/xls', views.export_perso_csv, name='export_perso_xls'),
]
