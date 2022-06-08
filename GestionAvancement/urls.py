from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('notation', views.notation, name='notation'),
    path('ajouternotation', views.ajouternotation, name='ajouternotation'),
    path('tboardavancement', views.tboardavancement, name='tboardavancement'),
    path('loadpersonnelavancement', views.loadpersonnelavancement, name='loadpersonnelavancement'),
]
