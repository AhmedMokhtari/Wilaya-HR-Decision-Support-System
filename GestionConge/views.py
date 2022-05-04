from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Conge, DateElimine
from GestionPersonnel.models import Personnel, Service, Servicepersonnel
from datetime import datetime
import numpy as np

# Create your views here.
@login_required(login_url='/connexion')
def conge (request):
    """
            nbiterationHoly = 0
            for item in dateelimine:
                if(item.dateelimine >= a1 and item.dateelimine <= a2):
                    nbiterationHoly = nbiterationHoly + 1
    """
    personnels = Personnel.objects.all()
    dateelimine = DateElimine.objects.all()
    # date1
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(datedebut__year=datetime.now().year).filter(datedebut__month=i + 1).count())
        i = i + 1


    if request.method == 'POST':
        perso = Personnel.objects.filter(idpersonnel=request.POST.get('perso')).first()
        datedecom = request.POST.get("datedecon")
        typede = request.POST["typede"]
        datere = request.POST.get('datere')
        a1 = datetime.strptime(datedecom, "%Y-%m-%d")
        a2 = datetime.strptime(datere, "%Y-%m-%d")
        data = [s.dateelimine.date() for s in dateelimine]
        datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
        nbjours = datenbjours
        objconge = Conge(type_conge=typede, datedebut=a1, dateretour=a2, idpersonnel_field=perso,nbjour=nbjours)
        objconge.save()
        return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'objconge': objconge ,'pubs':pubs})
    return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel,'pubs':pubs})
