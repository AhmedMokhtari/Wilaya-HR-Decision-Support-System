from django.urls import path
from . import views
urlpatterns = [
    path('ajouterconge', views.conge, name='ajouterconje'),
    path('consultation', views.GestionConge, name='consultationconge'),
    path('congeencours', views.GestionCongeEnCours, name='congeencours'),
    path('stopeconge/<int:id>', views.stopeConge, name='stopeconge'),
    path('deleteconge/<int:id>', views.delete, name='deleteconge'),
    path('persoinfo/<int:id>', views.persoinfo, name='persoinfo'),
    path('ajaxloadpersonnelforconge', views.ajaxloadpersonnelforconge, name='ajaxloadpersonnelforconge'),
]



