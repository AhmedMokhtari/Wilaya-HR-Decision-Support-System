from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from .models import *
from GestionPersonnel.models import Service,Division,Caidat,Cercle,Pashalik,District,Annexe,Entite
from django.http import JsonResponse,HttpResponse
from django.db.models import Q, Count
from fpdf.fpdf import FPDF
import json

def consultation2(request):
    liststages = []
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()
    stagepashalik = PashalikStage.objects.all().values('idstage_field__idstage', 'idstage_field__cin', 'idstage_field__nomstagiairear',
                                            "idstage_field__prenomstagiairear", 'idstage_field__nomstagiairefr', 'idstage_field__prenomstagiairefr',
                                            "idstage_field__sexe",'idpashalik_field__libellepashalikar'
                                            ,'idstage_field__datedebutstage', 'idstage_field__datefinstage')
    stageannexe = AnnexeStage.objects.all().values('idstage_field__idstage', 'idstage_field__cin', 'idstage_field__nomstagiairear',
                                            "idstage_field__prenomstagiairear", 'idstage_field__nomstagiairefr', 'idstage_field__prenomstagiairefr',
                                            "idstage_field__sexe",'idannexe_field__libelleannexear'
                                            ,'idstage_field__datedebutstage', 'idstage_field__datefinstage')
    stagecaidate = CaidatStage.objects.all().values('idstage_field__idstage', 'idstage_field__cin', 'idstage_field__nomstagiairear',
                                            "idstage_field__prenomstagiairear", 'idstage_field__nomstagiairefr', 'idstage_field__prenomstagiairefr',
                                            "idstage_field__sexe",'idcaidat_field__libellecaidatar'
                                            ,'idstage_field__datedebutstage', 'idstage_field__datefinstage')
    stageservice = ServiceStage.objects.all().values('idstage_field__idstage', 'idstage_field__cin', 'idstage_field__nomstagiairear',
                                            "idstage_field__prenomstagiairear", 'idstage_field__nomstagiairefr', 'idstage_field__prenomstagiairefr',
                                            "idstage_field__sexe",'idservice_field__libelleservicear'
                                            ,'idstage_field__datedebutstage', 'idstage_field__datefinstage')
    for stagiaire in stageservice:
        stageobj = {
            'idstage': stagiaire['idstage_field__idstage'],
            'cin': stagiaire['idstage_field__cin'],
            'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
            'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
            'sexe': stagiaire['idstage_field__sexe'],
            'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
            'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
            'idservice_field__libelleservicefr': stagiaire['idservice_field__libelleservicear']
        }
        if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'Terminé'})
        elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'En cours'})
        else:
            liststages.append({'stage': stageobj, 'statut': 'Pas commencer'})
    for stagiaire in stagepashalik:
        stageobj = {
            'idstage': stagiaire['idstage_field__idstage'],
            'cin': stagiaire['idstage_field__cin'],
            'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
            'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
            'sexe': stagiaire['idstage_field__sexe'],
            'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
            'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
            'idpashalik_field__libellepashalikfr': stagiaire['idpashalik_field__libellepashalikar']
        }
        if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'Terminé'})
        elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'En cours'})
        else:
            liststages.append({'stage': stageobj, 'statut': 'Pas commencer'})
    for stagiaire in stageannexe:
        stageobj = {
            'idstage': stagiaire['idstage_field__idstage'],
            'cin': stagiaire['idstage_field__cin'],
            'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
            'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
            'sexe': stagiaire['idstage_field__sexe'],
            'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
            'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
            'idannexe_field__libelleannexefr': stagiaire['idannexe_field__libelleannexear']
        }
        if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'Terminé'})
        elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'En cours'})
        else:
            liststages.append({'stage': stageobj, 'statut': 'Pas commencer'})
    for stagiaire in stagecaidate:
        stageobj = {
            'idstage': stagiaire['idstage_field__idstage'],
            'cin': stagiaire['idstage_field__cin'],
            'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
            'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
            'sexe': stagiaire['idstage_field__sexe'],
            'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
            'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
            'idcaidat_field__libellecaidatfr': stagiaire['idcaidat_field__libellecaidatar']
        }
        if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'Terminé'})
        elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
            liststages.append({'stage': stageobj, 'statut': 'En cours'})
        else:
            liststages.append({'stage': stageobj, 'statut': 'Pas commencer'})

    return render(request, 'GestionStagiaire/consultation2.html', {'entites': entites,'pashaliks':pashaliks,
                                  'cercles':cercles, 'districts':districts, 'divisions':divisions,'stagiaires': liststages})


def consultation(request):
    liststages = []
    divisions = Division.objects.all()
    stagiaires = Stage.objects.all().values('idstage', 'cin', 'nomstagiairear',
                                "prenomstagiairear", 'nomstagiairefr', 'prenomstagiairefr',
                                "sexe", "idservice_field__iddivision_field__libelledivisionfr",
                                'idservice_field__libelleservicefr','datedebutstage','datefinstage')
    for stagiaire in stagiaires:
        if stagiaire['datefinstage'] < datetime.now().astimezone() :
            liststages.append({'stage':stagiaire,'statut':'Terminé'})
        elif stagiaire['datedebutstage'] < datetime.now().astimezone():
            liststages.append({'stage':stagiaire,'statut':'En cours'})
        else: liststages.append({'stage':stagiaire,'statut':'Pas commencer'})
    return render(request,'GestionStagiaire/consultation.html',{'divisions':divisions,'stagiaires':liststages})

@csrf_exempt
def ajaxloadService(request):
    division = Division.objects.get(iddivision=request.POST.get('division'))
    objservices = {'services':list(Service.objects.filter(iddivision_field=division).values('idservice','libelleservicear','libelleservicefr'))}
    return JsonResponse(objservices, safe=False)

@csrf_exempt
def ajaxloadannexe(request):
    district = District.objects.get(iddistrict=request.POST.get('district', None))
    objannexe = {"annexes": list(
        Annexe.objects.filter(iddistrict_field=district).values('idannexe', 'libelleannexear', 'libelleannexefr'))}
    return JsonResponse(objannexe, safe=False)

@csrf_exempt
def ajaxloadcaida(request):
    cercle = Cercle.objects.get(idcercle=request.POST.get('cercle', None))
    objcaida = {"caidas": list(
        Caidat.objects.filter(idcercle_field=cercle).values('idcaidat', 'libellecaidatar', 'libellecaidatfr'))}
    return JsonResponse(objcaida, safe=False)

@csrf_exempt
def ajaxloaddivision(request):
    entite = Entite.objects.get(libelleentitefr=request.POST['entite'])
    objdivision = {"divisions": list(
        Division.objects.filter(identite_field=entite).values('iddivision', 'libelledivisionar', 'libelledivisionfr'))}
    return JsonResponse(objdivision, safe=False)

def filterstagiaire2(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr = selected_obj.split("&")
    if arr[2] == 'Homme':
        QSexe = Q(idstage_field__sexe='Homme-ذكر')
    elif arr[2] == 'Femme':
        QSexe = Q(idstage_field__sexe='Femme-أنثى')
    else:
        QSexe = ~Q(idstage_field__idstage=None)
    if arr[3] == 'yet':
        Qstatut = Q(idstage_field__datedebutstage__gt=datetime.now().astimezone())
    elif arr[3] == 'encours':
        Qstatut = Q(idstage_field__datedebutstage__lte=datetime.now().astimezone(), idstage_field__datefinstage__gte=datetime.now().astimezone())
    elif arr[3] == 'finished':
        Qstatut = Q(idstage_field__datefinstage__lt=datetime.now().astimezone())
    else:
        Qstatut = ~Q(idstage_field__idstage=None)
    liststagiaire = []
    if arr[0] == 'entite':
        if arr[1] == 'Secrétariat général':
            stageservice = ServiceStage.objects.filter(QSexe & Qstatut).values(
                'idstage_field__idstage',
                'idstage_field__cin',
                'idstage_field__nomstagiairear',
                "idstage_field__prenomstagiairear",
                'idstage_field__nomstagiairefr',
                'idstage_field__prenomstagiairefr',
                "idstage_field__sexe",
                'idservice_field__libelleservicear',
                'idstage_field__datedebutstage',
                'idstage_field__datefinstage')
            for stagiaire in stageservice:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idservice_field__libelleservicefr': stagiaire['idservice_field__libelleservicear']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
        elif arr[1] == 'Commandement':
            stagespashalik = PashalikStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                               'idstage_field__nomstagiairear',
                                                               "idstage_field__prenomstagiairear",
                                                               'idstage_field__nomstagiairefr',
                                                               'idstage_field__prenomstagiairefr',
                                                               "idstage_field__sexe",
                                                               'idpashalik_field__libellepashalikar',
                                                               'idstage_field__datedebutstage',
                                                               'idstage_field__datefinstage')
            stagesannexe = AnnexeStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                           'idstage_field__nomstagiairear',
                                                           "idstage_field__prenomstagiairear",
                                                           'idstage_field__nomstagiairefr',
                                                           'idstage_field__prenomstagiairefr',
                                                           "idstage_field__sexe", 'idannexe_field__libelleannexear'
                                                           , 'idstage_field__datedebutstage',
                                                           'idstage_field__datefinstage')
            stagecaidat = CaidatStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                            'idstage_field__nomstagiairear',
                                                            "idstage_field__prenomstagiairear",
                                                            'idstage_field__nomstagiairefr',
                                                            'idstage_field__prenomstagiairefr',
                                                            "idstage_field__sexe", 'idcaidat_field__libellecaidatar'
                                                            , 'idstage_field__datedebutstage',
                                                            'idstage_field__datefinstage')
            for stagiaire in stagespashalik:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idpashalik_field__libellepashalikfr': stagiaire['idpashalik_field__libellepashalikar']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
            for stagiaire in stagesannexe:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idannexe_field__libelleannexefr': stagiaire['idannexe_field__libelleannexear']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
            for stagiaire in stagecaidat:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idcaidat_field__libellecaidatfr': stagiaire['idcaidat_field__libellecaidatar']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif arr[0] == 'districtpashalik':
        if arr[1] == 'Pashalik':
            stagespashalik = PashalikStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                                'idstage_field__nomstagiairear',
                                                                "idstage_field__prenomstagiairear",
                                                                'idstage_field__nomstagiairefr',
                                                                'idstage_field__prenomstagiairefr',
                                                                "idstage_field__sexe",
                                                                'idpashalik_field__libellepashalikar'
                                                                , 'idstage_field__datedebutstage',
                                                                'idstage_field__datefinstage')
            for stagiaire in stagespashalik:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idpashalik_field__libellepashalikfr': stagiaire['idpashalik_field__libellepashalikar']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
        elif arr[1] == 'District':
            stagesannexe = AnnexeStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                            'idstage_field__nomstagiairear',
                                                            "idstage_field__prenomstagiairear",
                                                            'idstage_field__nomstagiairefr',
                                                            'idstage_field__prenomstagiairefr',
                                                            "idstage_field__sexe", 'idannexe_field__libelleannexear'
                                                            , 'idstage_field__datedebutstage',
                                                            'idstage_field__datefinstage')
            for stagiaire in stagesannexe:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idannexe_field__libelleannexefr': stagiaire['idannexe_field__libelleannexear']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
        else:
            stagecaidat = CaidatStage.objects.filter(QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                           'idstage_field__nomstagiairear',
                                                           "idstage_field__prenomstagiairear",
                                                           'idstage_field__nomstagiairefr',
                                                           'idstage_field__prenomstagiairefr',
                                                           "idstage_field__sexe", 'idcaidat_field__libellecaidatar'
                                                           , 'idstage_field__datedebutstage',
                                                           'idstage_field__datefinstage')
            for stagiaire in stagecaidat:
                stageobj = {
                    'idstage': stagiaire['idstage_field__idstage'],
                    'cin': stagiaire['idstage_field__cin'],
                    'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                    'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                    'sexe': stagiaire['idstage_field__sexe'],
                    'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                    'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                    'idcaidat_field__libellecaidatfr': stagiaire['idcaidat_field__libellecaidatar']
                }
                if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
                elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                    liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
                else:
                    liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})

    elif arr[0] == 'district':
        stagesannexe = AnnexeStage.objects.filter(Q(idannexe_field__iddistrict_field__iddistrict=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                        'idstage_field__nomstagiairear',
                                                        "idstage_field__prenomstagiairear",
                                                        'idstage_field__nomstagiairefr',
                                                        'idstage_field__prenomstagiairefr',
                                                        "idstage_field__sexe", 'idannexe_field__libelleannexear'
                                                        , 'idstage_field__datedebutstage',
                                                        'idstage_field__datefinstage')
        for stagiaire in stagesannexe:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idannexe_field__libelleannexefr': stagiaire['idannexe_field__libelleannexear']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif arr[0] == 'annexe':
        stagesannexe = AnnexeStage.objects.filter(
            Q(idannexe_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage',
                                                               'idstage_field__cin',
                                                               'idstage_field__nomstagiairear',
                                                               "idstage_field__prenomstagiairear",
                                                               'idstage_field__nomstagiairefr',
                                                               'idstage_field__prenomstagiairefr',
                                                               "idstage_field__sexe",
                                                               'idannexe_field__libelleannexear',
                                                               'idstage_field__datedebutstage',
                                                               'idstage_field__datefinstage')


        for stagiaire in stagesannexe:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idannexe_field__libelleannexefr': stagiaire['idannexe_field__libelleannexear']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif arr[0] == 'pashalik':
        stagespashalik = PashalikStage.objects.filter(Q(idpashalik_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage',
                                                                              'idstage_field__cin',
                                                                              'idstage_field__nomstagiairear',
                                                                              "idstage_field__prenomstagiairear",
                                                                              'idstage_field__nomstagiairefr',
                                                                              'idstage_field__prenomstagiairefr',
                                                                              "idstage_field__sexe",
                                                                              'idpashalik_field__libellepashalikar',
                                                                              'idstage_field__datedebutstage',
                                                                              'idstage_field__datefinstage')
        for stagiaire in stagespashalik:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idpashalik_field__libellepashalikfr': stagiaire['idpashalik_field__libellepashalikar']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif arr[0] == 'cercle':
        stagecaidat = CaidatStage.objects.filter(Q(idcaidat_field__idcercle_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                                         'idstage_field__nomstagiairear',
                                                                         "idstage_field__prenomstagiairear",
                                                                         'idstage_field__nomstagiairefr',
                                                                         'idstage_field__prenomstagiairefr',
                                                                         "idstage_field__sexe",
                                                                         'idcaidat_field__libellecaidatar'
                                                                         , 'idstage_field__datedebutstage',
                                                                         'idstage_field__datefinstage')
        for stagiaire in stagecaidat:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idcaidat_field__libellecaidatfr': stagiaire['idcaidat_field__libellecaidatar']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif arr[0] == 'caida':
        stagecaidat = CaidatStage.objects.filter(Q(idcaidat_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                                         'idstage_field__nomstagiairear',
                                                                         "idstage_field__prenomstagiairear",
                                                                         'idstage_field__nomstagiairefr',
                                                                         'idstage_field__prenomstagiairefr',
                                                                         "idstage_field__sexe",
                                                                         'idcaidat_field__libellecaidatar'
                                                                         , 'idstage_field__datedebutstage',
                                                                         'idstage_field__datefinstage')
        for stagiaire in stagecaidat:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idcaidat_field__libellecaidatfr': stagiaire['idcaidat_field__libellecaidatar']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif (arr[0] == 'division'):
        stageservice = ServiceStage.objects.filter(Q(idservice_field__iddivision_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage', 'idstage_field__cin',
                                                         'idstage_field__nomstagiairear',
                                                         "idstage_field__prenomstagiairear",
                                                         'idstage_field__nomstagiairefr',
                                                         'idstage_field__prenomstagiairefr',
                                                         "idstage_field__sexe", 'idservice_field__libelleservicear'
                                                         , 'idstage_field__datedebutstage',
                                                         'idstage_field__datefinstage')
        for stagiaire in stageservice:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idservice_field__libelleservicefr': stagiaire['idservice_field__libelleservicear']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})

    elif (arr[0] == 'service'):
        stageservice = ServiceStage.objects.filter(Q(idservice_field=arr[1]) & QSexe & Qstatut).values('idstage_field__idstage',
                                                            'idstage_field__cin',
                                                            'idstage_field__nomstagiairear',
                                                            "idstage_field__prenomstagiairear",
                                                            'idstage_field__nomstagiairefr',
                                                            'idstage_field__prenomstagiairefr',
                                                            "idstage_field__sexe",
                                                            'idservice_field__libelleservicear',
                                                            'idstage_field__datedebutstage',
                                                            'idstage_field__datefinstage')
        for stagiaire in stageservice:
            stageobj = {
                'idstage': stagiaire['idstage_field__idstage'],
                'cin': stagiaire['idstage_field__cin'],
                'nomstagiairear': stagiaire['idstage_field__nomstagiairear'],
                'prenomstagiairear': stagiaire['idstage_field__prenomstagiairear'],
                'sexe': stagiaire['idstage_field__sexe'],
                'nomstagiairefr': stagiaire["idstage_field__nomstagiairefr"],
                'prenomstagiairefr': stagiaire['idstage_field__prenomstagiairefr'],
                'idservice_field__libelleservicefr': stagiaire['idservice_field__libelleservicear']
            }
            if stagiaire['idstage_field__datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stagiaire['idstage_field__datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    data = json.dumps(liststagiaire)
    return JsonResponse({'data': data})


def filter_stagiaire(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr = selected_obj.split("&")
    if arr[2] == 'Homme':
        QSexe = Q(sexe='Homme-ذكر')
    elif arr[2] == 'Femme':
        QSexe = Q(sexe='Femme-أنثى')
    else:
        QSexe = ~Q(idstage=None)
    if arr[3] == 'yet':
        Qstatut = Q(datedebutstage__gt=datetime.now().astimezone())
    elif arr[3] == 'encours':
        Qstatut = Q(datedebutstage__lte=datetime.now().astimezone(),datefinstage__gte=datetime.now().astimezone())
    elif arr[3] == 'finished':
        Qstatut = Q(datefinstage__lt=datetime.now().astimezone())
    else:
        Qstatut = ~Q(idstage=None)
    liststagiaire = []
    if (arr[0]=='All'):
        stagiaire = Stage.objects.filter(QSexe & Qstatut).values('idstage', 'cin', 'nomstagiairear',
                                "prenomstagiairear", 'nomstagiairefr', 'prenomstagiairefr',
                                "sexe", 'datedebutstage','datefinstage',"idservice_field__iddivision_field__libelledivisionfr",
                                'idservice_field__libelleservicefr')
        for stage in stagiaire:
            stageobj = {
                'idstage': stage['idstage'],
                'cin': stage['cin'],
                'nomstagiairear': stage['nomstagiairear'],
                'prenomstagiairear': stage['prenomstagiairear'],
                'nomstagiairefr': stage["nomstagiairefr"],
                'prenomstagiairefr': stage['prenomstagiairefr'],
                'sexe': stage['sexe'],
                'idservice_field__iddivision_field__libelledivisionfr': stage[
                    'idservice_field__iddivision_field__libelledivisionfr'],
                'idservice_field__libelleservicefr': stage['idservice_field__libelleservicefr']
            }
            if stage['datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stage['datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif (arr[0]=='division'):
        stageiaire = Stage.objects.filter(Q(idservice_field__iddivision_field__iddivision=arr[1]) & QSexe & Qstatut).values(
                                'idstage', 'cin', 'nomstagiairear','prenomstagiairear','sexe', 'nomstagiairefr', 'prenomstagiairefr',
                                'datedebutstage','datefinstage', "idservice_field__iddivision_field__libelledivisionfr",
                                'idservice_field__libelleservicefr')
        for stage in stageiaire:
            stageobj = {
                'idstage': stage['idstage'],
                'cin': stage['cin'],
                'nomstagiairear': stage['nomstagiairear'],
                'prenomstagiairear': stage['prenomstagiairear'],
                'sexe': stage['sexe'],
                'nomstagiairefr': stage["nomstagiairefr"],
                'prenomstagiairefr': stage['prenomstagiairefr'],
                'idservice_field__iddivision_field__libelledivisionfr': stage[
                    'idservice_field__iddivision_field__libelledivisionfr'],
                'idservice_field__libelleservicefr': stage['idservice_field__libelleservicefr']
            }
            if stage['datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stage['datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    elif (arr[0] == 'service'):
        stagiaire = Stage.objects.filter(Q(idservice_field=arr[1]) & QSexe & Qstatut).values('idstage', 'cin', 'nomstagiairear',
                                "prenomstagiairear", 'nomstagiairefr', 'prenomstagiairefr',
                                "sexe",'datedebutstage','datefinstage', "idservice_field__iddivision_field__libelledivisionfr",
                                'idservice_field__libelleservicefr')
        for stage in stagiaire:
            stageobj = {
                'idstage': stage['idstage'],
                'cin': stage['cin'],
                'nomstagiairear': stage['nomstagiairear'],
                'sexe':stage['sexe'],
                'prenomstagiairear': stage['prenomstagiairear'],
                'nomstagiairefr': stage["nomstagiairefr"],
                'prenomstagiairefr': stage['prenomstagiairefr'],
                'idservice_field__iddivision_field__libelledivisionfr': stage[
                    'idservice_field__iddivision_field__libelledivisionfr'],
                'idservice_field__libelleservicefr': stage['idservice_field__libelleservicefr']
            }
            if stage['datefinstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'Terminé'})
            elif stage['datedebutstage'] < datetime.now().astimezone():
                liststagiaire.append({'stage': stageobj, 'statut': 'En cours'})
            else:
                liststagiaire.append({'stage': stageobj, 'statut': 'Pas commencer'})
    data = json.dumps(liststagiaire)
    return JsonResponse({'data': data})
def ajouter(request):
    divisions = Division.objects.all()
    if request.method == 'POST':
        nomar = request.POST['nomar']
        prenomar = request.POST['prenomar']
        nomfr = request.POST['nomfr']
        prenomfr = request.POST['prenomfr']
        cin = request.POST['cin']
        sexe = request.POST.get('sexe')
        email = request.POST['email']
        tele = request.POST['tele']
        datedebut = request.POST['datedebut']
        nbmois = request.POST['nbmois']
        service = request.POST.get('service')
        cinpdf = request.FILES.get('cinfile')
        cvpdf = request.FILES.get('cv')
        demandepdf = request.FILES.get('demande')
        assurancepdf = request.FILES.get('assurance')
        objservice = Service.objects.get(idservice=service)
        objstage = Stage(nomstagiairear=nomar, prenomstagiairear=prenomar, nomstagiairefr=nomfr,
                         prenomstagiairefr=prenomfr, cin=cin, sexe=sexe, email=email, tele=tele,
                         datedebutstage=datedebut, nbmois=nbmois, cinpdf=cinpdf, cvpdf=cvpdf,
                         demandepdf=demandepdf, assurancepdf=assurancepdf, idservice_field=objservice, datefinstage=datestage(datedebut, nbmois))
        objstage.save()
        return redirect(consultation)
    return render(request,'GestionStagiaire/ajouterstagiaire.html', {'divisions':divisions})


def modifier(request,id):
    objstage = Stage.objects.get(idstage=id)
    divisions = Division.objects.all()
    services = Service.objects.filter(iddivision_field=objstage.idservice_field.iddivision_field)
    if request.method == 'POST':
        objstage.nomstagiairear = request.POST['nomar']
        objstage.prenomstagiairear = request.POST['prenomar']
        objstage.nomstagiairefr = request.POST['nomfr']
        objstage.prenomstagiairefr = request.POST['prenomfr']
        objstage.cin = request.POST['cin']
        objstage.sexe = request.POST.get('sexe')
        objstage.email = request.POST['email']
        objstage.tele = request.POST['tele']
        objstage.datedebutstage = request.POST['datedebut']
        objstage.nbmois = request.POST['nbmois']
        objstage.datefinstage = datestage(request.POST['datedebut'],request.POST['nbmois'])
        objstage.idservice_field = Service.objects.get(idservice=request.POST.get('service'))
        if request.FILES.get('cinfile') is not None:
            objstage.cinpdf = request.FILES.get('cinfile')
        if request.FILES.get('cv') is not None:
            objstage.cvpdf = request.FILES.get('cv')
        if request.FILES.get('demande') is not None:
            objstage.demandepdf = request.FILES.get('demande')
        if request.FILES.get('assurance') is not None:
            objstage.assurancepdf = request.FILES.get('assurance')
        objstage.save()
        return redirect(consultation)
    return render(request,'GestionStagiaire/modifier.html', {'divisions':divisions, 'services':services, 'stagiaire':objstage})


def infostage(request, id):
    stagiaire = Stage.objects.get(idstage=id)
    return render(request,'GestionStagiaire/infostagiaire.html',{'stagiaire':stagiaire})

def tboardstagiaire(request):
    counthommes = Stage.objects.filter(sexe='Homme-ذكر').count()
    countfemmes = Stage.objects.filter(sexe='Femme-أنثى').count()
    divisions = Division.objects.values('iddivision','libelledivisionfr').all()[:9]
    stages = Stage.objects.all().values('idservice_field__iddivision_field__libelledivisionfr').annotate(scount=Count('idservice_field')).order_by('idservice_field__iddivision_field__libelledivisionfr')
    annees = Stage.objects.all().values('datedebutstage__year').distinct().order_by('-datedebutstage__year')
    countAll = Stage.objects.all().count()
    divs = Stage.objects.filter(datedebutstage__year=datetime.now().astimezone().year).values('idservice_field__iddivision_field__iddivision','idservice_field__iddivision_field__libelledivisionfr').annotate(scount=Count('idservice_field')).order_by('idservice_field__iddivision_field__libelledivisionfr')
    print(len(divs))
    listdiv = []
    for div in divisions:
        listdiv.append(divabbr(div['libelledivisionfr']))
    print(listdiv)
    listfinal = []
    for division in divisions:
        i = len(listfinal)
        for stage in stages:
            if division['libelledivisionfr'] == stage['idservice_field__iddivision_field__libelledivisionfr']:
                listfinal.append(f"{stage['scount']}")
        if(len(listfinal) == i):
            listfinal.append('0')
    return render(request,'GestionStagiaire/tboardstagiaire.html',{'counthommes':counthommes,
                                        'countfemmes':countfemmes, 'countAll':countAll, 'listdivs':listdiv,
                                        'stages':listfinal, 'annees':annees,'divisions':divs})

def tboardstagiaire2(request):
    counthommes = Stage.objects.filter(sexe='Homme-ذكر').count()
    countfemmes = Stage.objects.filter(sexe='Femme-أنثى').count()
    divisions = Division.objects.values('iddivision', 'libelledivisionfr').all()[:9]
    stages = Stage.objects.all().values('idservice_field__iddivision_field__libelledivisionfr').annotate(
        scount=Count('idservice_field')).order_by('idservice_field__iddivision_field__libelledivisionfr')
    annees = Stage.objects.all().values('datedebutstage__year').distinct().order_by('-datedebutstage__year')
    countAll = Stage.objects.all().count()
    divs = ServiceStage.objects.filter(idstage_field__datedebutstage__year=datetime.now().astimezone().year).count()
    pashalik = PashalikStage.objects.filter(idstage_field__datedebutstage__year=datetime.now().astimezone().year).count()
    cercle = CaidatStage.objects.filter(idstage_field__datedebutstage__year=datetime.now().astimezone().year).count()
    district = AnnexeStage.objects.filter(idstage_field__datedebutstage__year=datetime.now().astimezone().year).count()
    listdiv = []
    for div in divisions:
        listdiv.append(divabbr(div['libelledivisionfr']))
    print(listdiv)
    listfinal = []
    for division in divisions:
        i = len(listfinal)
        for stage in stages:
            if division['libelledivisionfr'] == stage['idservice_field__iddivision_field__libelledivisionfr']:
                listfinal.append(f"{stage['scount']}")
        if (len(listfinal) == i):
            listfinal.append('0')
    return render(request, 'GestionStagiaire/tboardstagiaire2.html', {'counthommes': counthommes,
                                                                     'countfemmes': countfemmes, 'countAll': countAll,
                                                                     'listdivs': listdiv,
                                                                     'stages': listfinal, 'annees': annees,
                                                                     'divisions': divs,
                                                                      'pashaliks':pashalik,
                                                                      'caidats':cercle,
                                                                      'districts':district
                                                                      })

def ajaxtboardfilterannee(request,*args,**kwargs):
    if kwargs.get('obj') == 'All':
        annee = ~Q(idstage=None)
    else:
        annee = Q(datedebutstage__year=int(kwargs.get('obj')))
    print(annee)
    divisions = Division.objects.all().values('libelledivisionfr')[:9]
    stages = Stage.objects.filter(annee).values('idservice_field__iddivision_field__libelledivisionfr').annotate(
        scount=Count('idservice_field')).order_by('idservice_field__iddivision_field__libelledivisionfr')
    listfinal = []
    for division in divisions:
        i = len(listfinal)
        for stage in stages:
            if division['libelledivisionfr'] == stage['idservice_field__iddivision_field__libelledivisionfr']:
                listfinal.append(f"{stage['scount']}")
        if (len(listfinal) == i):
            listfinal.append('0')
    data = json.dumps(listfinal)
    return JsonResponse({'data': data})

def tboardstagiarie2(request):
    return render(request,'GestionStagiaire/tboardstagiaire2.html')

def ajaxtboardfilterstate2(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr = selected_obj.split('&')
    Qdate = Q(datedebutstage__year=datetime.now().year)
    if arr[0] == 'All':
        org = 'All'
    if arr[0] == 'caidat':
        org = 'caidat'
        if arr[1] != 'All':
            Qorg = Q(idservice_field__iddivision_field__iddivision=int(arr[1]))
    if arr[0] == 'division':
        if arr[1] != 'All':
            Qorg = Q(idservice_field__iddivision_field__iddivision=int(arr[1]))
        else:
            Qorg = ~Q(idstage=None)
    if arr[0] == 'service':
        Qorg = Q(idservice_field__idservice=int(arr[1]))
    stagesPascommencer = Stage.objects.filter(Qorg & Qdate & Q(datedebutstage__gt=datetime.now().astimezone())).count()
    stageEncours = Stage.objects.filter(Qorg & Qdate & Q(datedebutstage__lte=datetime.now().astimezone(),
                                                         datefinstage__gte=datetime.now().astimezone())).count()
    stageTerminer = Stage.objects.filter(Qorg & Qdate & Q(datefinstage__lt=datetime.now().astimezone())).count()
    liststages = [stagesPascommencer, stageEncours, stageTerminer]
    data = json.dumps(liststages)
    return JsonResponse({'data': data})

def ajaxtboardfilterstate(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr = selected_obj.split('&')
    Qdate = Q(datedebutstage__year=datetime.now().year)

    if arr[0] == 'division':
        if arr[1] != 'All':
            Qdiv = Q(idservice_field__iddivision_field__iddivision=int(arr[1]))
        else:
            Qdiv = ~Q(idstage=None)
    if arr[0] == 'service':
        Qdiv = Q(idservice_field__idservice=int(arr[1]))
    stagesPascommencer = Stage.objects.filter(Qdiv&Qdate&Q(datedebutstage__gt=datetime.now().astimezone())).count()
    stageEncours = Stage.objects.filter(Qdiv & Qdate & Q(datedebutstage__lte=datetime.now().astimezone(),datefinstage__gte=datetime.now().astimezone())).count()
    stageTerminer = Stage.objects.filter(Qdiv & Qdate & Q(datefinstage__lt=datetime.now().astimezone())).count()
    liststages = [stagesPascommencer,stageEncours,stageTerminer]
    data = json.dumps(liststages)
    return JsonResponse({'data':data})

def ajaxstageservices(request,id):
    services = Stage.objects.filter(datedebutstage__year=datetime.now().astimezone().year,idservice_field__iddivision_field__iddivision=int(id)).values('idservice_field__idservice','idservice_field__libelleservicefr').annotate(scount=Count('idservice_field')).order_by('idservice_field__libelleservicefr')
    listservices = []
    for service in services:
        listservices.append({'service':service})
    return JsonResponse({'data':json.dumps(listservices)})


def attestationstage(request):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=9)
    pdf.text(21, 7, txt='ROYAUME DU MAROC')
    pdf.text(16, 12, txt='MINISTERE  DE L\'INTERIEUR')
    pdf.text(8, 17, txt='WILAYA DE LA REGION DE L\'ORIENTAL')
    pdf.text(13, 22, txt='PREFECTURE D\'OUJDA- ANGAD')
    pdf.text(19, 27, txt='SECRETARIAT GENERAL')
    pdf.text(8, 32, txt='DIVISION DES RESSOURCES HUMAINES')
    pdf.text(13, 37, txt='ET AFFAIRES ADMINISTRATIVES')
    pdf.text(14, 42, txt='N°:')
    pdf.set_font('Arial', 'B', size=16)
    pdf.text(74, 72, txt='ATTESTATION')
    pdf.rect(63, 63, 97, 13)
    pdf.set_font('Arial', size=16)
    pdf.set_y(95)
    pdf.set_x(20)
    pdf.multi_cell(175, 10, txt='  Dans le cadre des stages pratiques organisés à la Préfecture Oujda-Angad au profit des stagiaires des Instituts et des Ecoles de formation, Mlle, titulaire de la Carte d\'Identité Nationale N° F a effectué un stage pratique du 28/12/2020 au 26/02/2021 au Pachalik de la ville de Bni Drar.')
    pdf.set_y(180)
    pdf.set_x(20)
    pdf.multi_cell(175, 10, txt='   En foi de quoi, la présente attestation est délivrée à l\'intéressée sur sa demande  pour servir et valoir ce que de droit.')
    pdf.text(105, 224, txt='Oujda le:')
    pdf.output('attestationfull.pdf')
    pdfAF = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdfAF, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="mypdf.pdf"'
    return response