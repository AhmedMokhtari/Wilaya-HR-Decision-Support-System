from django.shortcuts import render,redirect
from .models import Personnel,Conjoint, Conjointpersonnel

#personnel -------------------------------.
def consultation(request):
    personnels = { 'personnels' : Personnel.objects.all()}
    return render(request, 'GestionPersonnel/consultation.html', personnels)



def gestion(request):
    if(request.method == 'POST'):
        nomfr = request.POST["nomfr"]
        nomar = request.POST["nomar"]
        prenomfr = request.POST["prenomfr"]
        prenomar = request.POST["prenomar"]
        cin = request.POST["cin"]
        daten = request.POST["daten"]
        lieunar = request.POST["lieunar"]
        lieunfr = request.POST["lieunfr"]
        tele = request.POST["tele"]
        email = request.POST["email"]
        situatfr = request.POST["situationffr"]
        situatar = request.POST["situationfar"]
        adressear= request.POST["adressear"]
        adressefr = request.POST["adressefr"]
        objperso= Personnel(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr, lieunaissancear=lieunar, lieunaissancefr=lieunfr, datenaissance=daten, tele=tele, email = email, situationfamilialear=situatar,situationfamilialefr=situatfr,adressear=adressear, adressefr=adressefr)
        objperso.save()
        conjoints = Conjointpersonnel.objects.filter(idpersonnel_field=objperso.idpersonnel).all()
    else:
        return render(request, 'GestionPersonnel/gestion.html')
    if (objperso):
        return render(request, 'GestionPersonnel/gestion.html', {'personnel': objperso, 'conjoints': conjoints})
    else:
        return render(request, 'GestionPersonnel/gestion.html')


#conjoint -----------------------------------
def conjoint(request):
    if request.method == 'POST':
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
        obj2 = Conjointpersonnel(idconjoint_field=con, idpersonnel_field=pers)
        obj2.save()

    else:
        cinpersonnel = request.GET.get('personnel', None)
        if(cinpersonnel) :
            return render(request, 'GestionPersonnel/conjoint.html', {'personnel': cinpersonnel})
        else:
            return render(request, 'GestionPersonnel/conjoint.html')
    if(obj1)  :
        return render(request, 'GestionPersonnel/conjoint.html', {'conjoint' : obj1 ,'personnel': pers.cin})
    else:
        return render(request, 'GestionPersonnel/conjoint.html')


