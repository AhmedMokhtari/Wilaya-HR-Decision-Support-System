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
    path('tboardconge', views.tboardconge, name='tboardconge'),
    path('tboardajaxfilterdivision/<str:obj>/', views.tboardfilterdiv, name='tboardajaxfilterdivision'),
    path('tboardajaxfiltercercle/<str:obj>/', views.tboardfiltercercle, name='tboardajaxfiltercercle'),
    path('tboardajaxfilterdistrict/<str:obj>/', views.tboardfilterdistrict, name='tboardajaxfilterdistrict'),
    path('tboardajaxfilterdivisionservice/<str:obj>/', views.tboardfilterdivse, name='tboardajaxfilterdivision'),
    path('tboardajaxfiltercaidat/<str:obj>/', views.tboardfiltercaidat, name='tboardajaxfiltercaidat'),
    path('tboardajaxfilterannexe/<str:obj>/', views.tboardfilterannexe, name='tboardajaxfilterannexe'),
    path('tboardajaxfilterpashaliktypeconge/<str:obj>/', views.tboardajaxfilterpashaliktypeconge, name='tboardajaxfilterpashaliktypeconge'),
    path('tboardajaxfiltersecretariattypeconge/<str:obj>/', views.tboardajaxfiltersecretariattypeconge, name='tboardajaxfiltersecretariattypeconge'),
    path('tboardajaxfiltercercletypeconge/<str:obj>/', views.tboardajaxfiltercercletypeconge, name='tboardajaxfiltercercletypeconge'),
    path('tboardajaxfilterdistricttypeconge/<str:obj>/', views.tboardajaxfilterdistricttypeconge, name='tboardajaxfilterdistricttypeconge'),
    path('tboardajaxfilterdivisiontypeconge/<str:obj>/', views.tboardajaxfilterdivisiontypeconge, name='tboardajaxfilterdivisiontypeconge'),
    path('tboardajaxfiltercaidattypeconge/<str:obj>/', views.tboardajaxfiltercaidattypeconge, name='tboardajaxfiltercaidattypeconge'),
    path('tboardajaxfilterannexetypeconge/<str:obj>/', views.tboardajaxfilterannexetypeconge, name='tboardajaxfilterannexetypeconge'),
    path('tboardcongedefaultyear/<str:obj>/', views.tboardcongedefaultyear,name='tboardcongedefaultyear'),
    path('tboardajaxfilterpashalik/<str:obj>/', views.tboardfilterpashalik, name='tboardajaxfilterpashalik'),
]



