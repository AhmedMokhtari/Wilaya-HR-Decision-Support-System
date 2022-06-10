from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('consultation', views.consultation, name='consultationpersonnel'),
    path('persoinfo', views.persoinfoimg, name='persoinfo'),
    path('perso-json/<str:obj>/', views.get_json_perso_data, name='perso-json'),
    path('ajouterp', views.ajouter, name='ajouterp'),
    path('ajouter_conjoint', views.ajouter_conjoint, name='ajouter_conjoint'),
    path('modifier_conjoint/<int:id>', views.modifier_conjoint, name='modifier_conjoint'),
    path('modifier/<int:id>', views.modifier,name="modifier"),
    path('export_pdf/<int:id>', views.printpdf, name='export_pdf'),
    path('export_pdfar/<int:id>', views.printpdfar, name='export_pdfar'),
    path('export_pdfquiter/<int:id>', views.printpdfquitter, name='export_pdfquiter'),
    path('taboard', views.taboardpersonnel, name='taboard'),
    path('ajouter_enfant', views.ajouter_enfant, name='ajouter_enfant'),
    path('modifier_enfant/<int:id>', views.modifier_enfant, name='modifier_enfant'),
    path('ajouter_diplome', views.ajouter_diplome, name='ajouter_diplome'),
    path('modifier_diplome/<int:id>', views.modifer_diplome, name='modifier_diplome'),
    path('deletereaffectation/<int:id>', views.deletereaffectation, name='deletereaffectation'),
    path('addreaffectation', views.addreaffectation, name='addreaffectation'),
    path('ajaxtaboardpersonnel', views.ajaxtaboardpersonnel, name='ajaxtaboardpersonnel'),
    path('ajaxajouterloadgrade', views.ajaxajouterloadgrade, name='ajaxajouterloadgrade'),
    path('ajaxajouterloadechellon', views.ajaxajouterloadechellon, name='ajaxajouterloadechellon'),
    path('ajaxajouterloadannexe', views.ajaxajouterloadannexe, name='ajaxajouterloadannexe'),
    path('ajaxajouterloadsevice', views.ajaxajouterloadsevice, name='ajaxajouterloadsevice'),
    path('ajaxajouterloadcaida', views.ajaxajouterloadcaida, name='ajaxajouterloadcaida'),
    path('ajaxloadpersonnel', views.ajaxloadpersonnel, name='ajaxloadpersonnel'),
    path('ajaxloadadministration', views.ajaxloadadministration, name='ajaxloadadministration'),
    path('ajaxajouterloaddivision', views.ajaxajouterloaddivision, name='ajaxajouterloaddivision'),
    path('reaffectation', views.reaffectation, name='reaffectation'),
    path('personnelinfo/<int:id>', views.personnelinfo, name='personnelinfo'),
]
