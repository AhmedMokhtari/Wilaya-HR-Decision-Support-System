import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from GestionPersonnel.models import *
from GestionAvancement.models import *
from .utils import *
from .models import Notation
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


@login_required(login_url='/')
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



@login_required(login_url='/')
def ajouternotation(request):
    perso=Personnel.objects.all()
    if request.method == "POST":
        persone=Personnel.objects.get(cin=request.POST["personneldata"])
        notation = Notation(note=request.POST["note"],annee=request.POST["annee"],idpersonnel_field=persone)
        notation.save()


    return render(request, 'GestionAvancement/ajouternotation.html', {'personnels': perso,})


@login_required(login_url='/')
def tboardavancement(request):
    grades = Grade.objects.all()
    return render(request, 'GestionAvancement/tboardavancememnt.html', {'grades': grades})

@login_required(login_url='/')
@csrf_exempt
def loadpersonnelavancement(request):
    grades = Grade.objects.get(idgrade=request.POST.get("grade"))
    personnels = Personnel.objects.all()
    listoutput = []
    datawarehouse = []
    for item in personnels:
        objgradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=item)
        if(objgradepersonnel.last() != None and objgradepersonnel.last().idgrade_field == grades):
            listoutput.append( objgradepersonnel.last())

    for item2 in listoutput:
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field,idgrade_field=item2.idgrade_field).first()
        date = item2.dateechellon + datetime.timedelta(30 * objrythme.rapide)
        note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year, annee__gte= item2.dateechellon.year)
        listnote = []
        for item3 in note:
            listnote.append(item3.note)
        moyenne = sum(listnote) / len(listnote)
        mois = 1
        if (item2.idgrade_field.gradefr == 'Administrateur adjoint' or item2.idgrade_field.gradefr == 'Administrateur'):
            if(item2.idechellon_field == '6' or item2.idechellon_field == '10' ):
                mois = 1
            else:
                if(moyenne>= 19 and moyenne <=20):
                    mois = objrythme.rapide
                elif(moyenne>= 18.75 and moyenne <=19):
                    mois = objrythme.rapide + 2
                elif (moyenne >= 18.25 and moyenne <= 18.50):
                    mois = objrythme.rapide + 3
                elif (moyenne >= 18 and moyenne <= 18.25):
                    mois = objrythme.rapide + 4
                elif (moyenne >= 17.75 and moyenne <= 18):
                    mois = objrythme.rapide + 5
                elif (moyenne >= 16.5 and moyenne <= 17.5):
                    mois = objrythme.rapide + 6
                elif (moyenne >= 16 and moyenne <= 16.5):
                    mois = objrythme.rapide + 5
                elif (moyenne >= 15.5 and moyenne <= 16):
                    mois = objrythme.rapide + 9
                elif (moyenne >= 15 and moyenne <= 15.5):
                    mois = objrythme.rapide + 12
                elif (moyenne >= 14.5 and moyenne <= 15):
                    mois = objrythme.rapide + 15
                elif (moyenne < 14.5):
                    mois = objrythme.rapide + 18
        else:
            if (moyenne >= 16 and moyenne <= 20):
                mois = objrythme.rapide
            elif (moyenne >= 10 and moyenne <= 16):
                mois = objrythme.moyen
            elif (moyenne < 10):
                mois = objrythme.lent

        datefin = item2.dateechellon + datetime.timedelta(30 * mois)
        indicebr = indice(item2.idgrade_field.idgrade)
        datamart = {'idpersonnel': item2.idpersonnel_field.idpersonnel,
                    'cin': item2.idpersonnel_field.cin,
                    'personnelnar': item2.idpersonnel_field.nomar,
                    'personnelnfr': item2.idpersonnel_field.nomfr,
                    'personnelpar': item2.idpersonnel_field.prenomar,
                    'personnelpfr': item2.idpersonnel_field.prenomfr,
                    'datefin': datefin.date(),
                    'datedebut': item2.dateechellon.date(),
                    'rythm': mois,
                    'grade': item2.idgrade_field.gradear,
                    'moyenne': f'{moyenne:.2f}',
                    'ppr': item2.idpersonnel_field.ppr,
                    'indicesebut': indicebr[item2.idechellon_field.idechellon - 1],
                    'indicesefin': indicebr[item2.idechellon_field.idechellon],
                    'echellondebut': item2.idechellon_field.echellon,
                    'echellondefin': Echellon.objects.get(idechellon=item2.idechellon_field.idechellon + 1).echellon}

        datawarehouse.append(datamart)
    return JsonResponse(datawarehouse, safe=False)