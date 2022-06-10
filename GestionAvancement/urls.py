from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('notation', views.notation, name='notation'),
    path('ajouternotation', views.ajouternotation, name='ajouternotation'),
    path('ajaxannee/<str:obj>/', views.ajaxAnnee, name='ajaxannees'),
    path('ajaxfilter/<str:obj>/', views.filter, name='ajaxfilter'),
    path('ajaxfilteryearmpty/<str:obj>/', views.get_json_perso_year_empty, name='ajaxfilteryearmpty'),
    path('tboardavancement', views.tboardavancement, name='tboardavancement'),
    path('loadpersonnelavancement', views.loadpersonnelavancement, name='loadpersonnelavancement'),
]
