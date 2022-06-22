from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('ajouter', views.ajouter, name='ajouterstagiaire'),
    path('consultation', views.consultation2, name='consultationstagiaire'),
    path('modifier/<int:id>', views.modifier, name="modifierstagiaire"),
    path('stage-json/<str:obj>/', views.filterstagiaire2, name='stage-json'),
    path('infos/<int:id>', views.infostage, name='infostagiaire'),
    path('tboardstagiaire', views.tboardstagiaire2, name='tboardstagiaire'),
    path('ajaxloadService', views.ajaxloadService, name='ajaxloadService'),
    path('ajaxloadannexe', views.ajaxloadannexe, name='ajaxloadannexe'),
    path('ajaxloadcaida', views.ajaxloadcaida, name='ajaxloadcaida'),
    path('ajaxloaddivision', views.ajaxloaddivision, name='ajaxloaddivision'),
    path('ajaxtboardfilterannee/<str:obj>/', views.ajaxtboardfilterannee, name='ajaxtboardfilterannee'),
    path('ajaxtboardfilterstate/<str:obj>/', views.ajaxtboardfilterstate, name='ajaxtboardfilterstate'),
    path('ajaxstageservices/<int:id>/', views.ajaxstageservices, name='ajaxstageservices'),
    path('attestationstage',views.attestationstage, name='attestationstage')
]
