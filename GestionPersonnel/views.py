from django.shortcuts import render
from .models import Personnel

# Create your views here.
def consultation(request):
    personnels = { 'personnels' : Personnel.objects.all()}
    return render(request, 'GestionPersonnel/consultation.html', personnels)

def ajouter_aff(request):
    return render(request, 'GestionPersonnel/ajouter.html')