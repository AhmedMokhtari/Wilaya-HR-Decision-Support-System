from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('connexion',views.connexion, name='connexion'),
    path('accueil', views.accueil, name='accueil'),
    path('test',views.test, name='test')
]
