from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('consultation',views.consultation,name = 'consultation'),
    path('gestion',views.gestion,name = 'gestion'),
    path('conjoint',views.conjoint,name = 'conjoint'),
    path('conjoint/personnel',views.conjoint,name = 'conjoint'),

]
