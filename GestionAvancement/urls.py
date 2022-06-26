from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('notation', views.notation, name='notation'),
    path('ajouternotation', views.ajouternotation, name='ajouternotation'),
    path('ajaxannee/<str:obj>/', views.ajaxannee, name='ajaxannees'),
    path('ajaxfilter/<str:obj>/', views.filter, name='ajaxfilter'),
    path('ajaxfilteryearmpty/<str:obj>/', views.get_json_perso_year_empty, name='ajaxfilteryearmpty'),
    path('avancementnormal', views.avancementnormal, name='avancementnormal'),
    path('loadpersonnelavancement', views.loadpersonnelavancement, name='loadpersonnelavancement'),
    path('pdfavencement', views.pdfavencement, name='pdfavencement'),
    path('pdfavencement/<int:id>/', views.pdfavencement, name='pdfavencement'),
    path('avancementexceptionel', views.avancementexceptionel, name='avancementexceptionel'),
    path('loadpersonnelavancementexeptionnel', views.loadpersonnelavancementexeptionnel, name='loadpersonnelavancementexeptionnel'),
    path('pdfavencementexceptionnel/<int:id>/', views.pdfavencementexceptionnel, name='pdfavencementexceptionnel'),
    path('pdfavencementexceptionnel', views.pdfavencementexceptionnel, name='pdfavencementexceptionnel'),
    path('ajouteravancementnormal', views.ajouteravancementnormal, name='ajouteravancementnormal'),
    path('ajouteravancementexceptionnel', views.ajouteravancementexceptionnel, name='ajouteravancementexceptionnel'),
    path('tboardavancement', views.tboardavancement, name='tboardavancement'),
    path('tboardavancementloadorga', views.tboardavancementloadorga, name='tboardavancementloadorga'),
]
