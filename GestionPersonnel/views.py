from django.shortcuts import render,redirect
from .models import Personnel,Conjoint, Conjointpersonnel

# Create your views here.
def consultation(request):
    personnels = { 'personnels' : Personnel.objects.all()}
    return render(request, 'GestionPersonnel/consultation.html', personnels)

def ajouter_aff(request):
    return render(request, 'GestionPersonnel/ajouter.html',)

def conjoint(request):
    if request == 'POST':
        nomfr = request.POST["nomfr"]
        nomar = request.POST["nomar"]
        prenomfr = request.POST["prenomfr"]
        prenomar = request.POST["prenomar"]
        cin = request.POST["cin"]
        daten = request.POST["daten"]
        lieun = request.POST["lieun"]
        personnelcin = request.POST["personnelcin"]
        obj1 = Conjoint(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr, lieunaissance=lieun, datenaissance=daten)
        obj1.save()

        pers = Personnel.objects.filter(cin= personnelcin).first()
        con = Conjoint.objects.filter(cin=cin).first()
        obj2 = Conjointpersonnel(idconjoint_field=con.idconjoint, idpersonnel_field=pers.idpersonnel)
        obj2.save()
    else:
        cinpersonnel = request.GET.get('personnel', None)
        if(cinpersonnel) :
            return render(request, 'GestionPersonnel/conjoint.html', {'personnel': cinpersonnel})
        else:
            return render(request, 'GestionPersonnel/conjoint.html')


