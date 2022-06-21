from datetime import *
from django.core import serializers
import json
import os
from fpdf import FPDF
from django.db import connection
import arabic_reshaper
from bidi.algorithm import get_display
from pathlib import Path
from django.db.models import Q
from operator import itemgetter
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from GestionPersonnel.models import *
from .utils import *
from .models import Notation
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta


@login_required(login_url='/')
@csrf_exempt
def tboardavancement(request):
    """objavancememnt = Avencement.objects.filter(dateechellon__year = datetime.now().year).filter(not idechellon_field__echellon='11')"""
    return render(request, "GestionAvancement/tboardavancement.html")


@login_required(login_url='/')
@csrf_exempt
def ajouteravancementnormal(request):
    json_data = json.loads(request.body)
    for item in json_data:
        if(item != None):
            datefin =datetime.strptime(item['datefin'], '%Y-%m-%d')
            if(datefin.year <= datetime.now().year):
                objavancement = Avencement.objects.create(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel']),
                                                          idgrade_field=Gradepersonnel.objects.filter(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().idgrade_field,
                                                          dategrade=Gradepersonnel.objects.filter(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().dategrade,
                                                          idechellon_field=Echellon.objects.get(idechellon=item['echellondefin']),
                                                          indice=item['indicesefin'],
                                                          dateechellon=item['datefin'])

                objGradepersonnel = Gradepersonnel.objects.create(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel']),
                                                            idgrade_field=Gradepersonnel.objects.filter(
                                                                idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().idgrade_field,
                                                            dategrade=Gradepersonnel.objects.filter(
                                                                idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().dategrade,
                                                            idechellon_field=Echellon.objects.get(idechellon=item['echellondefin']),
                                                            indice=item['indicesefin'],
                                                            dateechellon=item['datefin'])
                objavancement.save()
                objGradepersonnel.save()
    grades = Grade.objects.all()
    return render(request, 'GestionAvancement/avancementnormal.html', {'grades': grades})

@login_required(login_url='/')
@csrf_exempt
def ajouteravancementexceptionnel(request):
    json_data = json.loads(request.body)
    i = 0
    print(json_data['calcule']['div'])
    for item in json_data['datawarehouse']:
        if(item != None):
            if(i == int(json_data['calcule']['div'])):
                break;
            objavancement = Avencement.objects.create(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel']),
                                                      idgrade_field=Gradepersonnel.objects.filter(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().idgrade_field,
                                                      dategrade=Gradepersonnel.objects.filter(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().dategrade,
                                                      idechellon_field=Echellon.objects.get(idechellon=item['echellondefin']),
                                                      indice=item['indicesefin'],
                                                      dateechellon=item['datefin'])

            objGradepersonnel = Gradepersonnel.objects.create(idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel']),
                                                        idgrade_field=Gradepersonnel.objects.filter(
                                                            idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().idgrade_field,
                                                        dategrade=Gradepersonnel.objects.filter(
                                                            idpersonnel_field=Personnel.objects.get(idpersonnel=item['idpersonnel'])).last().dategrade,
                                                        idechellon_field=Echellon.objects.get(idechellon=item['echellondefin']),
                                                        indice=item['indicesefin'],
                                                        dateechellon=item['datefin'])
            objavancement.save()
            objGradepersonnel.save()
            i=i+1
    grades = Grade.objects.all()
    return render(request, 'GestionAvancement/avancementnormal.html', {'grades': grades})



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
    if request.method == "POST":
        persone = Personnel.objects.get(cin=request.POST["personneldata"])
        notation = Notation(note=request.POST["note"], annee=request.POST["annee"], idpersonnel_field=persone)
        notation.save()
    personnels = Personnel.objects.all()
    statutgrades = Statutgrade.objects.all()
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()
    persoId = Personnel.objects.all().values_list('idpersonnel', flat=True)
    listPerso = yearempty(persoId)
    return render(request, 'GestionAvancement/ajouternotation.html', {'personnels': personnels, 'divsions': divisions,
                                                            'persoempty': listPerso,
                                                            'entites': entites, 'pashaliks': pashaliks,
                                                            'districts': districts, 'statutgrades': statutgrades,
                                                            'cercles': cercles})


@login_required(login_url='/')
def avancementnormal(request):
    """personnel = Personnel.objects.all()
    for item in personnel:
        date = 2012
        while(date<=2022):
            notation = Notation.objects.create(annee=date,note=20,idpersonnel_field=item)
            notation.save()
            date = date + 1"""
    grades = Grade.objects.all()
    return render(request, 'GestionAvancement/avancementnormal.html', {'grades': grades})

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
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field, idgrade_field=item2.idgrade_field).first()
        if( objrythme != None):
            date = item2.dateechellon + relativedelta(months=objrythme.rapide)
            note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year, annee__gte= item2.dateechellon.year)
            listnote = []
            for item3 in note:
                listnote.append(item3.note)
            moyenne = sum(listnote) / len(listnote)
            mois = 0
            if (item2.idgrade_field.gradefr == 'Administrateur adjoint' or item2.idgrade_field.gradefr == 'Administrateur'):
                if(item2.idechellon_field.echellon == '6'):
                    mois = 1
                elif(item2.idechellon_field.echellon != '10'):
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
                if(item2.idechellon_field.echellon != '10'):
                    if (moyenne >= 16 and moyenne <= 20):
                        mois = objrythme.rapide
                    elif (moyenne >= 10 and moyenne <= 16):
                        mois = objrythme.moyen
                    elif (moyenne < 10):
                        mois = objrythme.lent

            if mois != 0 :
                datefin = item2.dateechellon + relativedelta(months=objrythme.rapide)
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
                            'echellondefin': Echellon.objects.get(
                                idechellon=item2.idechellon_field.idechellon + 1).echellon}
            else :
                datamart = None
        else:
            datamart = None
        datawarehouse.append(datamart)
    return JsonResponse(datawarehouse, safe=False)


def avancementexceptionel(request):
    """personnel = Personnel.objects.all()
        for item in personnel:
            date = 2012
            while(date<=2022):
                notation = Notation.objects.create(annee=date,note=20,idpersonnel_field=item)
                notation.save()
                date = date + 1"""
    grades = Grade.objects.all()
    return render(request, 'GestionAvancement/avancementexceptionel.html', {'grades': grades})

@login_required(login_url='/')
@csrf_exempt
def loadpersonnelavancementexeptionnel(request):
    grades = Grade.objects.get(idgrade=request.POST.get("grade"))

    personnels = Personnel.objects.all()
    listoutput = []
    datawarehouse = []
    for item in personnels:
        objgradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=item)
        if(objgradepersonnel.last() != None and objgradepersonnel.last().idgrade_field == grades):
            listoutput.append(objgradepersonnel.last())

    for item2 in listoutput:
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field, idgrade_field=item2.idgrade_field).first()
        if( objrythme != None):
            date = item2.dateechellon + relativedelta(months=objrythme.rapide)
            note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year, annee__gte= item2.dateechellon.year)
            listnote = []
            for item3 in note:
                listnote.append(item3.note)
            moyenne = sum(listnote) / len(listnote)
            mois = None
            if (item2.idgrade_field.gradefr == 'Technicien 2ème grade' or item2.idgrade_field.gradefr == 'Rédacteur 2ème grader'):
                if(item2.idechellon_field.echellon == '10'):
                    mois = 24
            elif(item2.idgrade_field.gradefr == 'Administrateur 2ème grade' or item2.idgrade_field.gradefr == 'Administrateur 3ème grade'
                 or item2.idgrade_field.gradefr == 'Administrateur' or item2.idgrade_field.gradefr == 'Administrateur adjoint'):
                if (item2.idechellon_field.echellon== '10'):
                    mois = 24
                elif(item2.idechellon_field.echellon== '10'):
                    mois = 1

            if(mois != None):
                datefin = item2.dateechellon + relativedelta(months=objrythme.rapide)
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
                            'echellondefin': Echellon.objects.get(
                                idechellon=item2.idechellon_field.idechellon + 1).echellon}
            else:
                datamart = None
        else:
            datamart = None
        datawarehouse.append(datamart)
    dataw = []
    for val in datawarehouse:
        if(val != None):
            dataw.append(val)

    value = round(int(request.POST.get("nb"))/10)
    valuemod = int(request.POST.get("nb"))%10
    calcule = {
        'div': value,
        'mod':  valuemod
    }
    dataw = sorted(dataw, key=lambda x: x['datefin'])
    return JsonResponse({'datawarehouse': dataw, 'calcule': calcule}, safe=False)

def ajaxannee(req,*args, **kwargs):
    cinPerso=kwargs.get('obj')
    personnel=Personnel.objects.get(cin=cinPerso)
    notationAnnee=Notation.objects.filter(idpersonnel_field=personnel).values_list('annee', flat=True)
    dateDemaration=Personnel.objects.get(cin=cinPerso)
    #dateDemarationYear = datetime.strptime(str(dateDemaration.datedemarcation), '%Y-%m-%d %H:%M:%S%z')
    yearnoww= datetime.now().year
    dateDemarationYear = datetime(yearnoww-10,1, 1)
    yearNow = datetime.now().year
    listyearempty=[]
    listyear=[]
    for a in range(dateDemarationYear.year,yearNow+1):
        listyear.append(a)
    for a in listyear:
        if a not in list(notationAnnee):
            listyearempty.append(a)
    data = json.dumps(listyearempty)
    return JsonResponse({'data': data})


# filter -------------------------------.
@login_required(login_url='/connexion')
def filter(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr=selected_obj.split("&")
    listPerso = []
    if(arr[0]=='entite'):
        if(arr[1]=='Secrétariat général'):
               QOrganisme=Q(organisme='Service')
               perso = Personnel.objects.filter(QOrganisme).values_list('cin', flat=True)
               listPerso =list(perso)
        elif(arr[1]=='Commandement'):
            orgPashalik=Q(organisme='pashalik')
            orgCaida=Q(organisme='Caida')
            orgAnnexe=Q(organisme='Annexe')
            persoPashalik = Personnel.objects.filter(orgPashalik).values_list('cin', flat=True)
            persoCaida = Personnel.objects.filter(orgCaida).values_list('cin', flat=True)
            persoAnnexe = Personnel.objects.filter(orgAnnexe).values_list('cin', flat=True)
            #res = {**list(persoPashalik), **list(persoCaida), **list(persoAnnexe)}
            listPerso=list(persoPashalik)
            listPerso.extend(list(persoCaida))
            listPerso.extend(list(persoAnnexe))
        elif (arr[1] == 'Cabinet'):
            ServicePer = Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            CabinetId = Division.objects.get(libelledivisionfr='Cabinet')
            servCabinet = Service.objects.filter(iddivision_field=CabinetId).values_list('idservice', flat=True)
            idServ = [user for user in PersoService if user['idservice_field'] in servCabinet]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
        elif (arr[1] == 'Dai'):
            ServicePer = Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            daiId = Division.objects.get(libelledivisionfr='Dai')
            servDai = Service.objects.filter(iddivision_field=daiId).values_list('idservice', flat=True)
            idServ = [user for user in PersoService if user['idservice_field'] in servDai]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso=list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
        elif (arr[1] == 'Dsic'):
            ServicePer=Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            DsicId= Division.objects.get(libelledivisionfr='DSIC')
            servDsic=Service.objects.filter(iddivision_field=DsicId).values_list('idservice', flat=True)
            superplayers = [user for user in PersoService if user['idservice_field'] in servDsic]
            listofid=[]
            for a in superplayers:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso=Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal=[]
            for it in  listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
    elif(arr[0]=='division'):
        ServicePer = Servicepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        serv = Service.objects.filter(iddivision_field=arr[1]).values_list('idservice', flat=True)
        superplayers = [user for user in PersoService if user['idservice_field'] in serv]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        QOrganisme=Q(organisme='Service')
        listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin', flat=True))
    elif (arr[0] == 'service'):
        ServicePer = Servicepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idservice_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        QOrganisme=Q(organisme='Service')
        listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin', flat=True))
    elif (arr[0] == 'districtpashalik'):
        if(arr[1]=='Pashalik'):
            persoPashalik = Personnel.objects.filter(organisme='pashalik').values_list('cin', flat=True)
            listPerso=list(persoPashalik)
        elif(arr[1]=='Cercle'):
            persoCaida = Personnel.objects.filter(organisme='Caida').values_list('cin', flat=True)
            listPerso=list(persoCaida)
        elif(arr[1]=='District'):
            persoAnnexe = Personnel.objects.filter(organisme='Annexe').values_list('cin', flat=True)
            listPerso=list(persoAnnexe)
    elif (arr[0] == 'district'):
        ServicePer = Annexepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        servAnnex = Annexe.objects.filter(iddistrict_field=arr[1]).values_list('idannexe',flat=True)
        superplayers = [user for user in PersoService if user['idannexe_field'] in servAnnex]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgAnnexe=Q(organisme='Annexe')
        listidperso = Personnel.objects.filter(orgAnnexe).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso=list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
    elif (arr[0] == 'cercle'):
        ServicePer = Caidatpersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                'idcaidat_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        servCaida = Caidat.objects.filter(idcercle_field=arr[1]).values_list('idcaidat',flat=True)
        superplayers = [user for user in PersoService if user['idcaidat_field'] in servCaida]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgCaida=Q(organisme='Caida')
        listidperso = Personnel.objects.filter(orgCaida).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso=list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
    elif (arr[0] == 'annexe'):
        ServicePer = Annexepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idannexe_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgAnnexe=Q(organisme='Annexe')
        listidperso = Personnel.objects.filter(orgAnnexe).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin', flat=True))
    elif (arr[0] == 'pashalik'):
        ServicePer = Pashalikpersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                'idpashalik_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idpashalik_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgPashalik=Q(organisme='pashalik')
        listidperso = Personnel.objects.filter(orgPashalik).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso=list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin',flat=True))
    elif (arr[0] == 'caida'):
        caidaPer = Caidatpersonnel.objects.all()
        caidaid = caidaPer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in caidaid:
            x = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                'idcaidat_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idcaidat_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgCaida=Q(organisme='Caida')
        listidperso = Personnel.objects.filter(orgCaida).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = list(Personnel.objects.filter(idpersonnel__in=listfinal).values_list('cin', flat=True))
   ##data = serializers.serialize("json",listPerso )
    data=json.dumps(listPerso)
    return JsonResponse({'data': data})

@login_required(login_url='/connexion')
def get_json_perso_year_empty(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr=selected_obj.split("&")
    listPerso = []
    if(arr[0]=='entite'):
        if(arr[1]=='Secrétariat général'):
               QOrganisme=Q(organisme='Service')
               perso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
               listPerso =yearempty(perso)
        elif(arr[1]=='Commandement'):
            orgPashalik=Q(organisme='pashalik')
            orgCaida=Q(organisme='Caida')
            orgAnnexe=Q(organisme='Annexe')
            persoPashalik = Personnel.objects.filter(orgPashalik).values_list('idpersonnel', flat=True)
            persoCaida = Personnel.objects.filter(orgCaida).values_list('idpersonnel', flat=True)
            persoAnnexe = Personnel.objects.filter(orgAnnexe).values_list('idpersonnel', flat=True)
            #res = {**list(persoPashalik), **list(persoCaida), **list(persoAnnexe)}
            listPerso=yearempty(persoPashalik)
            listCaida=yearempty(persoCaida)
            listAnnexe=yearempty(persoAnnexe)
            listPerso.extend(list(listCaida))
            listPerso.extend(list(listAnnexe))
        elif (arr[1] == 'Cabinet'):
            ServicePer = Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            CabinetId = Division.objects.get(libelledivisionfr='Cabinet')
            servCabinet = Service.objects.filter(iddivision_field=CabinetId).values_list('idservice', flat=True)
            idServ = [user for user in PersoService if user['idservice_field'] in servCabinet]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso = yearempty(listfinal)
        elif (arr[1] == 'Dai'):
            ServicePer = Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            daiId = Division.objects.get(libelledivisionfr='Dai')
            servDai = Service.objects.filter(iddivision_field=daiId).values_list('idservice', flat=True)
            idServ = [user for user in PersoService if user['idservice_field'] in servDai]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso = yearempty(listfinal)
        elif (arr[1] == 'Dsic'):
            ServicePer=Servicepersonnel.objects.all()
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x)
            DsicId= Division.objects.get(libelledivisionfr='DSIC')
            servDsic=Service.objects.filter(iddivision_field=DsicId).values_list('idservice', flat=True)
            superplayers = [user for user in PersoService if user['idservice_field'] in servDsic]
            listofid=[]
            for a in superplayers:
                listofid.append(a['idpersonnel_field'])
            QOrganisme = Q(organisme='Service')
            listidperso=Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
            listfinal=[]
            for it in  listidperso:
                if it in listofid:
                    listfinal.append(it)
            listPerso = yearempty(listfinal)
    elif(arr[0]=='division'):
        ServicePer = Servicepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        serv = Service.objects.filter(iddivision_field=arr[1]).values_list('idservice', flat=True)
        superplayers = [user for user in PersoService if user['idservice_field'] in serv]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        QOrganisme=Q(organisme='Service')
        listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'service'):
        ServicePer = Servicepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idservice_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        QOrganisme=Q(organisme='Service')
        listidperso = Personnel.objects.filter(QOrganisme).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'districtpashalik'):
        if(arr[1]=='Pashalik'):
            persoPashalik = Personnel.objects.filter(organisme='pashalik').values_list('idpersonnel', flat=True)
            listPerso = yearempty(persoPashalik)
        elif(arr[1]=='Cercle'):
            persoCaida = Personnel.objects.filter(organisme='Caida').values_list('idpersonnel', flat=True)
            listPerso = yearempty(persoCaida)
        elif(arr[1]=='District'):
            persoAnnexe = Personnel.objects.filter(organisme='Annexe').values_list('idpersonnel', flat=True)
            listPerso = yearempty(persoAnnexe)
    elif (arr[0] == 'district'):
        ServicePer = Annexepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        servAnnex = Annexe.objects.filter(iddistrict_field=arr[1]).values_list('idannexe',flat=True)
        superplayers = [user for user in PersoService if user['idannexe_field'] in servAnnex]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgAnnexe=Q(organisme='Annexe')
        listidperso = Personnel.objects.filter(orgAnnexe).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'cercle'):
        ServicePer = Caidatpersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                'idcaidat_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        servCaida = Caidat.objects.filter(idcercle_field=arr[1]).values_list('idcaidat',flat=True)
        superplayers = [user for user in PersoService if user['idcaidat_field'] in servCaida]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgCaida=Q(organisme='Caida')
        listidperso = Personnel.objects.filter(orgCaida).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'annexe'):
        ServicePer = Annexepersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idannexe_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgAnnexe=Q(organisme='Annexe')
        listidperso = Personnel.objects.filter(orgAnnexe).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'pashalik'):
        ServicePer = Pashalikpersonnel.objects.all()
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                'idpashalik_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idpashalik_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgPashalik=Q(organisme='pashalik')
        listidperso = Personnel.objects.filter(orgPashalik).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
    elif (arr[0] == 'caida'):
        caidaPer = Caidatpersonnel.objects.all()
        caidaid = caidaPer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in caidaid:
            x = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                'idcaidat_field',
                'idpersonnel_field').last()
            PersoService.append(x)
        superplayers = [user for user in PersoService if user['idcaidat_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        orgCaida=Q(organisme='Caida')
        listidperso = Personnel.objects.filter(orgCaida).values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it)
        listPerso = yearempty(listfinal)
   ##data = serializers.serialize("json",listPerso )
    data=json.dumps(listPerso)
    return JsonResponse({'data': data})



def pdfavencement(request, id):
    grade = Grade.objects.get(idgrade=id)
    annee = str(datetime.now().year)
    BASE_DIR = Path(__file__).resolve().parent.parent
    fontdir = os.path.join(BASE_DIR, 'static/filefonts')
    pdf = FPDF(orientation='L')
    pdf.add_font('TradArab', '', os.path.join(fontdir, 'TradArab.ttf'), uni=True)
    pdf.add_font('TradArabB', '', os.path.join(fontdir, 'TradArabB.ttf'), uni=True)
    pdf.add_page()
    pdf.set_font('TradArabB',size=11)
    pdf.text(269-10, 7, txt=get_display(arabic_reshaper.reshape('المملكة المغربية')))
    pdf.text(271-11, 12, txt=get_display(arabic_reshaper.reshape("وزارة الداخلية")))
    pdf.text(271-12, 17, txt=get_display(arabic_reshaper.reshape('ولاية جهة الشرق')))
    pdf.text(274-15, 22, txt=get_display((arabic_reshaper.reshape('عمالة وجدة أنكاد'))))
    pdf.text(269-15, 27, txt=get_display(arabic_reshaper.reshape('مجلس عمالة وجدة أنكاد')))
    pdf.text(270-15, 32, txt=get_display(arabic_reshaper.reshape('المديرية العامة للمصالح')))
    pdf.text(270-15, 37, txt=get_display(arabic_reshaper.reshape('مصلحة الموارد البشرية')))
    pdf.set_font('TradArabB',size=15)
    pdf.text(85-len(grade.gradear)-len(annee),64,txt=get_display(arabic_reshaper.reshape(f'مشروع لائحة الترسيم و الترقية في الرتبة في درجة {grade.gradear} لوزارة الداخلية برسم سنة {annee} والسنوات السابقة')))
    pdf.set_fill_color(r=191, g=191, b=191)
    pdf.ln(75)
    pdf.set_left_margin(0)
    pdf.set_x(0)
    pdf.set_font('TradArabB',size=8)
    pdf.cell(17,24,txt=get_display(arabic_reshaper.reshape('ملاحظات')), border=1, align='C', fill=True)
    #pdf.set_x(35)
    pdf.multi_cell(22,12,txt=get_display(arabic_reshaper.reshape(' المتساوية الأعضاء   رأي اللجنة الإدارية')),border=1,align='C', fill=True)
    pdf.set_y(85)
    pdf.set_x(39)
    pdf.cell(69,12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية الجديدة درجة {grade.gradear}')), border=1,align='C', fill=True, ln=2)
    pdf.cell(34,12,txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')), border=1, fill=True,align='C')
    pdf.cell(24,12,txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')), border=1, fill=True, align='C')
    pdf.cell(11,12,txt=get_display(arabic_reshaper.reshape('الرتبة')), border=1, fill=True, align='C', ln=2)
    pdf.set_y(85)
    pdf.set_x(108)
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النقطة')),border=1,fill=True, align='C')
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النسق')),border=1,fill=True, align='C')
    pdf.cell(69, 12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية القديمة درجة {grade.gradear}')), border=1, align='C', fill=True, ln=2)
    pdf.cell(34, 12, txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')), border=1, fill=True, align='C')
    pdf.cell(24, 12, txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')), border=1, fill=True, align='C')
    pdf.cell(11, 12, txt=get_display(arabic_reshaper.reshape('الرتبة')), border=1, fill=True, align='C', ln=2)
    pdf.set_y(85)
    pdf.set_x(201)
    pdf.cell(19,24, txt="Nom",border=1,fill=True, align='C')
    pdf.cell(19, 24, txt="Prenom", border=1, fill=True, align='C')
    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('الاسم العائلي')), border=1, fill=True, align='C')
    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('الاسم الشخصي')), border=1, fill=True, align='C')
    pdf.cell(14,24, txt=get_display(arabic_reshaper.reshape('رقم التاجير')), border=1, fill=True, align='C')
    #pdf.cell(18, 18, txt=get_display(arabic_reshaper.reshape('1234567891011')), border=1, fill=True, align='C')
    pdf.cell(15, 24, txt="Cin", border=1, fill=True, align='C')
    pdf.set_x(0)
    y = 109
    pdf.set_y(y)
    pdf.set_auto_page_break(True,20)

    grades = Grade.objects.get(idgrade=id)
    personnels = Personnel.objects.all()
    listoutput = []
    for item in personnels:
        objgradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=item)
        if (objgradepersonnel.last() != None and objgradepersonnel.last().idgrade_field == grades):
            listoutput.append(objgradepersonnel.last())

    for item2 in listoutput:
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field,
                                          idgrade_field=item2.idgrade_field).first()
        if(objrythme != None):
            date = item2.dateechellon + relativedelta(months=objrythme.rapide)
            note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year,
                                           annee__gte=item2.dateechellon.year)
            listnote = []
            for item3 in note:
                listnote.append(item3.note)
            moyenne = sum(listnote) / len(listnote)
            mois = None
            if (item2.idgrade_field.gradefr == 'Administrateur adjoint' or item2.idgrade_field.gradefr == 'Administrateur'):
                if (item2.idechellon_field == '6'):
                    mois = 1
                elif(item2.idechellon_field != '6'):
                    if (moyenne >= 19 and moyenne <= 20):
                        mois = objrythme.rapide
                    elif (moyenne >= 18.75 and moyenne <= 19):
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
                if (item2.idechellon_field.echellon != '10'):
                    if (moyenne >= 16 and moyenne <= 20):
                        mois = objrythme.rapide
                    elif (moyenne >= 10 and moyenne <= 16):
                        mois = objrythme.moyen
                    elif (moyenne < 10):
                        mois = objrythme.lent

            if (mois != None):
                datefin = item2.dateechellon + relativedelta(months=mois)
                if datefin.year <= datetime.now().year:
                    decision1 = 'يترقى'
                    decision2 = 'يترقى'
                else:
                    decision1 = 'يؤجل'
                    decision2 = 'يؤجل'
                indicebr = indice(item2.idgrade_field.idgrade)
                pdf.cell(17, 10, txt=get_display(arabic_reshaper.reshape(decision1)), border=1, align='C')
                pdf.cell(22, 10, txt=get_display(arabic_reshaper.reshape(decision2)), border=1, align='C')
                pdf.cell(34, 10, txt=datefin.date().isoformat(), border=1, align='C')
                pdf.cell(24, 10, txt=indicebr[item2.idechellon_field.idechellon], border=1, align='C')
                pdf.cell(11, 10, txt=Echellon.objects.get(idechellon=item2.idechellon_field.idechellon + 1).echellon, border=1, align='C')
                pdf.cell(12, 10, txt=f'{moyenne:.2f}', border=1, align='C')
                pdf.cell(12, 10, txt=str(mois), border=1, align='C')
                pdf.cell(34, 10, txt=item2.dateechellon.date().isoformat(), border=1, align='C')
                pdf.cell(24, 10, txt=indicebr[item2.idechellon_field.idechellon - 1], border=1, align='C')
                pdf.cell(11, 10, txt=item2.idechellon_field.echellon, border=1, align='C')
                pdf.cell(19, 10, txt=item2.idpersonnel_field.nomfr, border=1, align='C')
                pdf.cell(19, 10, txt=item2.idpersonnel_field.prenomfr, border=1, align='C')
                pdf.cell(15, 10, txt=get_display(arabic_reshaper.reshape(item2.idpersonnel_field.nomar)), border=1, align='C')
                pdf.cell(15, 10, txt=get_display(arabic_reshaper.reshape(item2.idpersonnel_field.prenomar)), border=1, align='C')
                pdf.cell(14, 10, txt=item2.idpersonnel_field.ppr, border=1, align='C')
                pdf.cell(15, 10, txt=item2.idpersonnel_field.cin, border=1, align='C')
                if y >= 189:
                    y = 10
                else:
                    y = y + 10
                    pdf.set_y(y)


    pdfAF = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdfAF, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="pdfavencement.pdf"'
    return response



def pdfavencementexceptionnel(request):
    grade = Grade.objects.get(idgrade=request.GET.get('id', None))
    annee = str(datetime.now().year)
    BASE_DIR = Path(__file__).resolve().parent.parent
    fontdir = os.path.join(BASE_DIR, 'static/filefonts')
    pdf = FPDF(orientation='L')
    pdf.add_font('TradArab', '', os.path.join(fontdir, 'TradArab.ttf'), uni=True)
    pdf.add_font('TradArabB', '', os.path.join(fontdir, 'TradArabB.ttf'), uni=True)
    pdf.add_page()
    pdf.set_font('TradArabB',size=11)
    pdf.text(269-10, 7, txt=get_display(arabic_reshaper.reshape('المملكة المغربية')))
    pdf.text(271-11, 12, txt=get_display(arabic_reshaper.reshape("وزارة الداخلية")))
    pdf.text(271-12, 17, txt=get_display(arabic_reshaper.reshape('ولاية جهة الشرق')))
    pdf.text(274-15, 22, txt=get_display((arabic_reshaper.reshape('عمالة وجدة أنكاد'))))
    pdf.text(269-15, 27, txt=get_display(arabic_reshaper.reshape('مجلس عمالة وجدة أنكاد')))
    pdf.text(270-15, 32, txt=get_display(arabic_reshaper.reshape('المديرية العامة للمصالح')))
    pdf.text(270-15, 37, txt=get_display(arabic_reshaper.reshape('مصلحة الموارد البشرية')))
    pdf.set_font('TradArabB',size=15)
    pdf.text(85-len(grade.gradear)-len(annee),64,txt=get_display(arabic_reshaper.reshape(f'مشروع لائحة الترسيم و الترقية في الرتبة الاستثنائية في درجة {grade.gradear} لوزارة الداخلية برسم سنة {annee} والسنوات السابقة')))
    pdf.set_fill_color(r=191, g=191, b=191)
    pdf.ln(75)
    pdf.set_left_margin(0)
    pdf.set_x(0)
    pdf.set_font('TradArabB',size=8)
    pdf.cell(17,24,txt=get_display(arabic_reshaper.reshape('ملاحظات')), border=1, align='C', fill=True)
    #pdf.set_x(35)
    pdf.multi_cell(22,12,txt=get_display(arabic_reshaper.reshape(' المتساوية الأعضاء   رأي اللجنة الإدارية')),border=1,align='C', fill=True)
    pdf.set_y(85)
    pdf.set_x(39)
    pdf.cell(69,12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية الجديدة درجة {grade.gradear}')), border=1,align='C', fill=True, ln=2)
    pdf.cell(34,12,txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')), border=1, fill=True,align='C')
    pdf.cell(24,12,txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')), border=1, fill=True, align='C')
    pdf.cell(11,12,txt=get_display(arabic_reshaper.reshape('الرتبة')), border=1, fill=True, align='C', ln=2)
    pdf.set_y(85)
    pdf.set_x(108)
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النقطة')),border=1,fill=True, align='C')
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النسق')),border=1,fill=True, align='C')
    pdf.cell(69, 12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية القديمة درجة {grade.gradear}')), border=1, align='C', fill=True, ln=2)
    pdf.cell(34, 12, txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')), border=1, fill=True, align='C')
    pdf.cell(24, 12, txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')), border=1, fill=True, align='C')
    pdf.cell(11, 12, txt=get_display(arabic_reshaper.reshape('الرتبة')), border=1, fill=True, align='C', ln=2)
    pdf.set_y(85)
    pdf.set_x(201)
    pdf.cell(19,24, txt="Nom",border=1,fill=True, align='C')
    pdf.cell(19, 24, txt="Prenom", border=1, fill=True, align='C')
    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('الاسم العائلي')), border=1, fill=True, align='C')
    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('الاسم الشخصي')), border=1, fill=True, align='C')
    pdf.cell(14,24, txt=get_display(arabic_reshaper.reshape('رقم التاجير')), border=1, fill=True, align='C')
    #pdf.cell(18, 18, txt=get_display(arabic_reshaper.reshape('1234567891011')), border=1, fill=True, align='C')
    pdf.cell(15, 24, txt="Cin", border=1, fill=True, align='C')
    pdf.set_x(0)
    y = 109
    pdf.set_y(y)
    pdf.set_auto_page_break(True,20)

    grades = Grade.objects.get(idgrade=request.GET.get('id', None))
    personnels = Personnel.objects.all()
    i=0
    datawarehouse = []
    listoutput = []
    for item in personnels:
        objgradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=item)
        if (objgradepersonnel.last() != None and objgradepersonnel.last().idgrade_field == grades):
            listoutput.append(objgradepersonnel.last())

    for item2 in listoutput:
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field,
                                          idgrade_field=item2.idgrade_field).first()
        if(objrythme != None):
            date = item2.dateechellon + relativedelta(months = objrythme.rapide)
            note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year,
                                           annee__gte=item2.dateechellon.year)
            listnote = []
            for item3 in note:
                listnote.append(item3.note)
            moyenne = sum(listnote) / len(listnote)
            mois = None
            if (item2.idgrade_field.gradefr == 'Technicien 2ème grade' or item2.idgrade_field.gradefr == 'Rédacteur 2ème grader'):
                if (item2.idechellon_field.echellon == '10'):
                    mois = 1
            elif (item2.idgrade_field.gradefr == 'Administrateur 2ème grade' or item2.idgrade_field.gradefr == 'Administrateur 3ème grade'):
                if (item2.idechellon_field.echellon == '10'):
                    mois = 24

            if (mois != None):
                datefin = item2.dateechellon + relativedelta(months=mois)
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
                            'mois': mois,
                            'grade': item2.idgrade_field.gradear,
                            'moyenne': f'{moyenne:.2f}',
                            'ppr': item2.idpersonnel_field.ppr,
                            'indicesebut': indicebr[item2.idechellon_field.idechellon - 1],
                            'indicesefin': indicebr[item2.idechellon_field.idechellon],
                            'echellondebut': item2.idechellon_field.echellon,
                            'echellondefin': Echellon.objects.get(
                                idechellon=item2.idechellon_field.idechellon + 1).echellon}
                datawarehouse.append(datamart)

    dataw = sorted(datawarehouse, key=lambda x: x['datefin'])

    for item in dataw:
        datefin = item['datefin']
        if datefin.year <= datetime.now().year:
            if (i < int(request.GET.get('first', None))):
                decision1 = 'يترقى'
                decision2 = 'يترقى'
            else:
                decision1 = 'يؤجل'
                decision2 = 'يؤجل'
        else:
            decision1 = 'يؤجل'
            decision2 = 'يؤجل'
        i = i + 1
        pdf.cell(17, 10, txt=get_display(arabic_reshaper.reshape(decision1)), border=1, align='C')
        pdf.cell(22, 10, txt=get_display(arabic_reshaper.reshape(decision2)), border=1, align='C')
        pdf.cell(34, 10, txt=str(item['datefin']), border=1, align='C')
        pdf.cell(24, 10, txt=item['indicesebut'], border=1, align='C')
        pdf.cell(11, 10, txt=get_display(arabic_reshaper.reshape('إستثنائية')), border=1,
                 align='C')
        pdf.cell(12, 10, txt=item['moyenne'], border=1, align='C')
        pdf.cell(12, 10, txt=str(item['mois']), border=1, align='C')
        pdf.cell(34, 10, txt=str(item['datedebut']), border=1, align='C')
        pdf.cell(24, 10, txt=item['indicesefin'], border=1, align='C')
        pdf.cell(11, 10, txt=item['echellondebut'], border=1, align='C')
        pdf.cell(19, 10, txt=item['personnelnfr'], border=1, align='C')
        pdf.cell(19, 10, txt=item['personnelpfr'], border=1, align='C')
        pdf.cell(15, 10, txt=get_display(arabic_reshaper.reshape(item['personnelnar'])), border=1, align='C')
        pdf.cell(15, 10, txt=get_display(arabic_reshaper.reshape(item['personnelpar'])), border=1,
                 align='C')
        pdf.cell(14, 10, txt=item['ppr'], border=1, align='C')
        pdf.cell(15, 10, txt=item['cin'], border=1, align='C')
        if y >= 189:
            y = 10
        else:
            y = y + 10
            pdf.set_y(y)

    value = round(int(request.GET.get("nb")) / 10)
    valuemod = int(request.GET.get("nb")) % 10

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('	الحصيص	')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(value), border=1, align='C')

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('	الخارج	')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(value), border=1, align='C')

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('	الباقي	')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(valuemod), border=1, align='C')

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('المقسوم عليه')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(10), border=1, align='C')

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('عدد المستوفين لشروط الترقي في الرتبة')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(10), border=1, align='C')

    pdf.cell(15, 24, txt=get_display(arabic_reshaper.reshape('عدد المناصب في السلك المقيدة في الميزانية')), border=1,
             fill=True, align='C')
    pdf.cell(30, 36, txt=str(request.GET.get('nb')), border=1, align='C')


    pdfAF = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdfAF, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="pdfavencement.pdf"'
    return response