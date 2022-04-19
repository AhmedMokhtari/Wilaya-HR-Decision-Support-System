from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Conge
from GestionPersonnel.models import Personnel

# Create your views here.

@login_required(login_url='/connexion')
def conge (request):
    personnels = Personnel.objects.all()
    if request.method == 'POST':
        data =request.POST.get('perso')
        perso = Personnel.objects.filter(cin = data)
        datedecom = request.POST["datedecon"]
        typede = request.POST["typede"]
        nbjours = request.POST.get('nbjours')
        congeob = Conge(type_conge=typede, datedebut=datedecom, nbjour=int(nbjours))
        congeob.save()

    return render(request, 'GestionConge/conge.html', {'personnels': personnels})
