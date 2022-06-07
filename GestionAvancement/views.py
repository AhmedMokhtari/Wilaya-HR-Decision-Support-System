from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from GestionPersonnel.models  import *
from .models import Notation
# Create your views here.


@login_required(login_url='/connexion')
def notation(request):
    perso=Personnel.objects.all()
    grades = Grade.objects.all()
    statutgrades = Statutgrade.objects.all()
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()

    listPerso=[]
    idperso =perso.order_by('idpersonnel').values_list('idpersonnel', flat=True).distinct()
    for id in idperso:
        a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel','cin','ppr','nomfr','prenomfr','administrationapp','sexe','organisme','photo').first()
        b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                                 'idgrade_field__idstatutgrade_field__statutgradefr').last()
        c={}
        if(a['organisme']):
            if(a['organisme']=='Service'):
                c = Servicepersonnel.objects.filter(idpersonnel_field=id).values('idservice_field__libelleservicear',
                                                                               'idservice_field__libelleservicefr',
                                                                               'idservice_field__iddivision_field__libelledivisionfr',
                                                                               'idservice_field__iddivision_field__libelledivisionar').last()
            elif(a['organisme']=='Annexe'):
                c = Annexepersonnel.objects.filter(idpersonnel_field=id).values('idannexe_field__libelleannexear',
                                                                                 'idannexe_field__libelleannexefr',
                                                                                 'idannexe_field__iddistrict_field__libelledistrictar',
                                                                                 'idannexe_field__iddistrict_field__libelledistrictfr').last()
            elif (a['organisme'] == 'Caida'):
                c = Caidatpersonnel.objects.filter(idpersonnel_field=id).values('idcaidat_field__libellecaidatar',
                                                                                'idcaidat_field__libellecaidatfr').last()
            elif (a['organisme'] == 'pashalik'):
                c = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values('idpashalik_field__libellepashalikar',
                                                                            'idpashalik_field__libellepashalikfr').last()
        if (not b):
            b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
        if(not c):
            c={'idservice_field__libelleservicear':'', 'idservice_field__libelleservicefr':'', 'idservice_field__libelleservicefr':'', 'idservice_field__iddivision_field__libelledivisionar':''}

        res={**a, **b,**c}
        listPerso.append(res)

    gradeperso = Gradepersonnel.objects.order_by('idpersonnel_field').values('idpersonnel_field','idpersonnel_field__cin','idpersonnel_field__ppr','idpersonnel_field__nomfr','idpersonnel_field__prenomfr','idpersonnel_field__administrationapp','idpersonnel_field__sexe','idpersonnel_field__organisme','idgrade_field__gradefr','idgrade_field__idstatutgrade_field__statutgradefr')

    return render(request, 'GestionAvancement/notation.html', {'divsions': divisions,
                                                                  'grades': grades, 'gradeperso': gradeperso,
                                                                  'listPerso': listPerso, 'entites': entites,
                                                                  'pashaliks': pashaliks, 'districts':districts,
                                                                  'statutgrades': statutgrades, 'cercles': cercles})



@login_required(login_url='/connexion')
def ajouter(request):
    perso=Personnel.objects.all()
    if request.method == "POST":
        persone=Personnel.objects.get(cin=request.POST["personneldata"])
        notation = Notation(note=request.POST["note"],annee=request.POST["annee"],idpersonnel_field=persone)
        notation.save()


    return render(request, 'GestionAvancement/conge.html', {'personnels': perso,})
