from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('notation', views.notation, name='notation'),
    path('ajouter', views.ajouter, name='ajouter'),

]
