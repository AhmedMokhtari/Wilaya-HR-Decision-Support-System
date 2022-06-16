from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from GestionPersonnel.models import *
import collections
from pydash import at
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.db import connection
from datetime import date, datetime, timedelta
from django.db.models import Q,Sum
from .utils import *
import json
from django.db.models import Count



@login_required(login_url='/')
def GestionConge(request):
    """
            nbiterationHoly = 0
            for item in dateelimine:
                if(item.dateelimine >= a1 and item.dateelimine <= a2):
                    nbiterationHoly = nbiterationHoly + 1
    """
    personnels = Personnel.objects.all()
    dateelimine = DateElimine.objects.all()
    conges = Conge.objects.all()
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(
            Conge.objects.filter(datedebut__year=datetime.now().year).filter(datedebut__month=i + 1).count())
        i = i + 1
    try:
        sql = 'select d.LibelleDivisionAr,d.LibelleDivisionFr, count(c.IdConge) as total from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision'
        cursor = connection.cursor()
        cursor.execute(sql)
        divisions = list(cursor.fetchall())
    except Exception as e:
        exception = str(e)
    finally:
        cursor.close

    if request.method == 'POST':
        perso = Personnel.objects.filter(idpersonnel=request.POST.get('perso')).first()
        datedecom = request.POST.get("datedecon")
        typede = request.POST["typede"]
        nbjours = int(request.POST["nbjours"])

        a1 = datetime.strptime(datedecom, "%Y-%m-%d")
        a2 = datetime.strptime(datedecom, "%Y-%m-%d")
        data = [s.dateelimine.date() for s in dateelimine]
        while (i < nbjours):
            if(date.today().weekday() != 5 and date.today().weekday() != 6 and a2 in data):
                a1 = a1 + timedelta(days=nbjours)
        datere = a1
        objconge = Conge(type_conge=typede, datedebut=a2, dateretour=datere, idpersonnel_field=perso, nbjour=nbjours)
        objconge.save()

        return render(request, 'GestionConge/gestionConge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'objconge': objconge, 'conges': conges, 'divisions': divisions})
    return render(request, 'GestionConge/gestionConge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges,'divisions': divisions})


@login_required(login_url='/')
def persoinfo(request,id):
    objpersonnel=Personnel.objects.get(idpersonnel=id);
    print(objpersonnel)
    congeperso=Conge.objects.filter(idpersonnel_field=id);
    listannee =[]
    annee =congeperso.order_by('annee').values_list('annee', flat=True).distinct()
    Q1 = Q(idpersonnel_field=id)
    for a in annee :
        Q2 = Q(annee=a)
        b ={'anneesum':Conge.objects.filter(Q1 & Q2).aggregate(Sum('nbjour'))}
        listannee.append(b)
    return render(request, 'GestionConge/persoinfo.html',{'objpersonnel':objpersonnel,'listdate': zip(annee,listannee),'congeperso':congeperso})

@login_required(login_url='/')
def GestionCongeEnCours(request):
    Q1 = Q(statut='En Cours')
    Q2 = Q(dateretour__gt= datetime.now())
    congesEncour = Conge.objects.filter(Q1 & Q2)
    print(congesEncour)
    listdate =[]
    dateelimine = DateElimine.objects.all()
    for a in congesEncour:
        d1 = datetime.strptime(str(a.dateretour.strftime('%Y/%m/%d')), "%Y/%m/%d")
        d2 = datetime.strptime(str(date.today().strftime('%Y/%m/%d')), "%Y/%m/%d")
        delta = d1 - d2;
        datedecom = a.dateretour
        a2 = datetime.strptime(str(datedecom.strftime('%Y/%m/%d')), "%Y/%m/%d")
        a1 = datetime.now()
        data = [s.dateelimine.date() for s in dateelimine]
        datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
        b={'joursrestan':delta.days,'joursrestanConge':datenbjours}
        listdate.append(b);
    cursor = connection.cursor()
    cursor.execute('''select * from Conge where Statut='En Cours' and dateRetour <= GETDATE() ''')
    EncourFini = dictfetchall(cursor)
    if(request.method=='POST'):
        id=request.POST.getlist('id[]')
        Conge.objects.filter(idconge__in=id).update(statut='Terminer')
    '''dateelimine = DateElimine.objects.all()
    datedecom = congesEncour.dateretour
    a1 = datetime.strptime(str(datedecom.strftime('%Y/%m/%d')), "%Y/%m/%d")
    a2 = datetime.now()
    data = [s.dateelimine.date() for s in dateelimine]
    datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
    objconge.nbjour = datenbjours;'''
    return render(request, 'GestionConge/congeEnCours.html', {'congesEnCours':zip(congesEncour,listdate),'enCoursFini':EncourFini})


@login_required(login_url='/')
def persoinfo(request, id):
    objpersonnel=Personnel.objects.get(idpersonnel=id)
    print(objpersonnel)
    congeperso=Conge.objects.filter(idpersonnel_field=id)
    annee =congeperso.order_by('dateaffectation').values_list('annee', flat=True).distinct()
    listannee = []
    Q1 = Q(idpersonnel_field=id)
    for a in annee:
        Q2 = Q(annee=a)
        b = {'anneesum': Conge.objects.filter(Q1 & Q2).aggregate(Sum('nbjour'))}
        listannee.append(b)
    return render(request, 'GestionConge/persoinfo.html',{'objpersonnel':objpersonnel,'listdate': zip(annee,listannee),'congeperso':congeperso})


@login_required(login_url='/')
def conge(request):
    """
            nbiterationHoly = 0
            for item in dateelimine:
                if(item.dateelimine >= a1 and item.dateelimine <= a2):
                    nbiterationHoly = nbiterationHoly + 1
    """
    personnels = Personnel.objects.all()
    dateelimine = DateElimine.objects.all()
    conges = Conge.objects.all()
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(
            Conge.objects.filter(datedebut__year=datetime.now().year).filter(datedebut__month=i + 1).count())
        i = i + 1
    try:
        sql = 'select d.LibelleDivisionAr,d.LibelleDivisionFr, count(c.IdConge) as total from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision'
        cursor = connection.cursor()
        cursor.execute(sql)
        divisions = list(cursor.fetchall())
    except Exception as e:
        exception = str(e)
    finally:
        cursor.close

    if request.method == 'POST':
        perso = Personnel.objects.filter(cin=request.POST.get('personneldata')).first()
        datedecom = request.POST.get("datedecon")
        typede = request.POST["typede"]
        nbjours = int(request.POST["nbjours"])
        a1 = datetime.strptime(datedecom, "%Y-%m-%d")
        a2 = datetime.strptime(datedecom, "%Y-%m-%d")


        dater =  findWorkingDayAfter(a1,nbjours)
        objconge = Conge(type_conge=typede, datedebut=a2, dateretour=dater, idpersonnel_field=perso, nbjour=nbjours)
        objconge.save()

        return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'objconge': objconge, 'conges': conges, 'divisions': divisions})
    return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges, 'divisions': divisions})

@login_required(login_url='/')
def stopeConge(request,id):
    print(id)
    dateelimine = DateElimine.objects.all()
    objconge = Conge.objects.get(idconge=id)
    print(objconge)
    objconge.statut="Terminer";
    objconge.dateretour= datetime.now();
    datedecom =objconge.datedebut
    a1 = datetime.strptime(str(datedecom.strftime('%Y/%m/%d')),"%Y/%m/%d")
    a2 = datetime.now()
    data = [s.dateelimine.date() for s in dateelimine]
    datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
    objconge.nbjour=datenbjours;
    objconge.save();
    Q1 = Q(statut='En Cours')
    Q2 = Q(dateretour__gt=datetime.now())
    congesEncour = Conge.objects.filter(Q1 & Q2)
    print(congesEncour)
    listdate = []
    for a in congesEncour:
        d1 = datetime.strptime(str(a.dateretour.strftime('%Y/%m/%d')), "%Y/%m/%d")
        d2 = datetime.strptime(str(date.today().strftime('%Y/%m/%d')), "%Y/%m/%d")
        delta = d1 - d2;
        b = {'joursrestan': delta.days}
        listdate.append(b);
    cursor = connection.cursor()
    cursor.execute('''select * from Conge where Statut='En Cours' and dateRetour <= GETDATE() ''')
    EncourFini = dictfetchall(cursor)
    if (request.method == 'POST'):
        id = request.POST.getlist('id[]')
        Conge.objects.filter(idconge__in=id).update(statut='Terminer')

    return render(request, 'GestionConge/congeEnCours.html',
                  {'congesEnCours': zip(congesEncour, listdate), 'enCoursFini': EncourFini})

@login_required(login_url='/')
def delete(request,id):
    objconge = Conge.objects.get(idconge=id)
    objconge.delete()
    response = redirect('/conge/ajouterconge')
    return response


@login_required(login_url='/connexion')
@csrf_exempt
def ajaxloadpersonnelforconge(request):
    personnel = Personnel.objects.filter(cin=request.POST.get('personnel', None))
    if(personnel != None):
        objconge = {'persodata': list(personnel.values('idpersonnel', 'nomar', 'prenomar', 'cin', 'ppr', 'sexe')),
                    'congean': str(CalculateYearConge('رخصة إدارية',personnel)),
                    'congeparen': str(CalculateYearConge('رخصة الأبوة',personnel)),
                    'congemere': str(CalculateYearConge('رخصة الأمومة',personnel)),
                    'congestit': str(CalculateYearConge('رخصة إستثنائية', personnel)),
                    'congehaj': str(CalculateYearConge('رخصة الحج', personnel)),
                    }
        return JsonResponse(objconge, safe=False)
    else:
        objconge = {'persodata'}
        return JsonResponse(objconge, safe=False)

def tboardconge(request):
    personnels = Personnel.objects.all()
    dateelimine = DateElimine.objects.all()
    conges = Conge.objects.all()
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(
            Conge.objects.filter(datedebut__year=datetime.now().year).filter(datedebut__month=i + 1).count())
        i = i + 1
    try:
        sql = "select d.LibelleDivisionAr,d.LibelleDivisionFr, count(c.IdConge) as total from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel  inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# where p.organisme='Service' group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision"
        cursor = connection.cursor()
        cursor.execute(sql)
        divisions = list(cursor.fetchall())
    except Exception as e:
        exception = str(e)
    finally:
        cursor.close
    congeAdmiCount=Conge.objects.filter(type_conge='رخصة إدراية').count()
    congeExpCount=Conge.objects.filter(type_conge='رخصة استثنائية').count()
    congeHajCount=Conge.objects.filter(type_conge='رخصة الحج').count()
    congeMotCount=Conge.objects.filter(type_conge='رخصة الأموة').count()
    congeFatCount=Conge.objects.filter(type_conge='الرخصة الأبوية').count()

    congeScCount = Conge.objects.filter(idpersonnel_field__organisme='Service').count()
    congePsCount = Conge.objects.filter(idpersonnel_field__organisme='pashalik').count()
    congeDsCount = Conge.objects.filter(idpersonnel_field__organisme='Annexe').count()
    congeCrCount = Conge.objects.filter(idpersonnel_field__organisme='Caida').count()
    congeids=Conge.objects.filter(idpersonnel_field__organisme='Service').values_list('idpersonnel_field',flat=True)
    ## Group Conge By  Service
    groupByService=(Servicepersonnel.objects.filter(idpersonnel_field__in=congeids)
     .values('idservice_field__libelleservicear','idservice_field__libelleservicefr')
     .annotate(dcount=Count('idservice_field'))
     .order_by()
     )
    #######################
    ## Group Conge By  Division
    groupByDivision=(Servicepersonnel.objects.filter(idpersonnel_field__in=congeids)
     .values('idservice_field__iddivision_field__libelledivisionar','idservice_field__iddivision_field__libelledivisionfr')
     .annotate(dcount=Count('idservice_field__iddivision_field'))
     .order_by()
     )
    #######################
    #Group by Type Conge
    result = (Conge.objects
              .values('type_conge')
              .annotate(dcount=Count('type_conge'))
              .order_by()
              )
    #######################################""
    congeCount=Conge.objects.all().count()
    congeAdmiCountPer=(congeAdmiCount/congeCount)*100
    congeMotCountPer=(congeMotCount/congeCount)*100
    congeFatCountPer=(congeFatCount/congeCount)*100
    congeHajCountPer=(congeHajCount/congeCount)*100
    congeExpCountPer=(congeExpCount/congeCount)*100

    context={'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges,'divisions': divisions,"Sc":congeScCount,'Ps':congePsCount,'Cr':congeCrCount,'Ds':congeDsCount,
            'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount ,'congeFatCount':congeFatCount,
             'congeAdmiCountPer':'{:.2f}'.format(congeAdmiCountPer),'congeMotCountPer':'{:.2f}'.format(congeMotCountPer),'congeFatCountPer':'{:.2f}'.format(congeFatCountPer),'congeExpCountPer':'{:.2f}'.format(congeExpCountPer),'congeHajCountPer':'{:.2f}'.format(congeHajCountPer)}
    return render (request,'GestionConge/tboardconges.html', context)

def tboardfilterdiv(req,*args, **kwargs):
    '''groupByDivision = (Servicepersonnel.objects.filter(idpersonnel_field__in=congeids)
                       .values('idservice_field__iddivision_field__libelledivisionar',
                               'idservice_field__iddivision_field__libelledivisionfr')
                       .annotate(dcount=Count('idservice_field__iddivision_field'))
                       .order_by()
                       )'''
    congeids=Conge.objects.filter(idpersonnel_field__organisme='Service').values_list('idpersonnel_field',flat=True)
    listPerso=[]
    for id in congeids:
        objj=Servicepersonnel.objects.filter(idpersonnel_field=id).values('idpersonnel_field','idservice_field__iddivision_field__libelledivisionar',
                                                                          'idservice_field__iddivision_field__libelledivisionfr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idservice_field__iddivision_field__libelledivisionfr'] for d in listPerso])
    groupByDivision=[]
    for key, value in dict(count).items():
        divar=Division.objects.get(libelledivisionfr=key)
        val={'idservice_field__iddivision_field__libelledivisionfr':key,'idservice_field__iddivision_field__libelledivisionar':divar.libelledivisionar,'dcount':value}
        groupByDivision.append(val)
    '''sql = "select d.LibelleDivisionAr as idservice_field__iddivision_field__libelledivisionar,d.LibelleDivisionFr as idservice_field__iddivision_field__libelledivisionfr, count(c.IdConge) as dcount from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel  inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# where p.organisme='Service' group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision"
    cursor = connection.cursor()
    cursor.execute(sql)
    #groupByDivision = cursor.fetchall()
    groupByDivision = dictfetchall(cursor)
    print(groupByDivision)'''
    data = json.dumps(groupByDivision)
    return JsonResponse({'data': data})
def tboardfilterdivse(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeids=Conge.objects.filter(idpersonnel_field__organisme='Service').values_list('idpersonnel_field',flat=True)
    Qdiv = Q(idservice_field__iddivision_field__libelledivisionfr=obj)
    '''groupByService = (Servicepersonnel.objects.filter(Qperso & Qdiv)
                      .values('idservice_field__libelleservicear', 'idservice_field__libelleservicefr')
                      .annotate(dcount=Count('idservice_field'))
                      .order_by()
                      )'''
    idsdiv=Servicepersonnel.objects.filter(Qdiv).values_list('idpersonnel_field',flat=True)
    listfinal=[]
    for a in congeids:
        if a in idsdiv:
            listfinal.append(a)
    listPerso = []
    for id in listfinal:
        Qid=Q(idpersonnel_field=id)
        objj = Servicepersonnel.objects.filter(Qid & Qdiv ).values('idpersonnel_field',
                                                                   'idservice_field__libelleservicear',
                                                                   'idservice_field__libelleservicefr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idservice_field__libelleservicefr'] for d in listPerso])
    groupByService = []
    for key, value in dict(count).items():
        servar = Service.objects.get(libelleservicefr=key)
        val = {'idservice_field__libelleservicefr': key,
               'idservice_field__libelleservicear': servar.libelleservicear, 'dcount': value}
        groupByService.append(val)

    '''sql = "select S.LibellServicenAr as idservice_field__libelleservicear,S.LibelleServiceFr as idservice_field__libelleservicefr, count(c.IdConge) as dcount from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel  inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# where p.organisme='Service' and d.LibelleDivisionFr= {obj} group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision".format(obj = obj)
    cursor = connection.cursor()
    cursor.execute(sql)
    # groupByDivision = cursor.fetchall()
    groupByDivision = dictfetchall(cursor)
    data = json.dumps(list(groupByDivision))'''
    data = json.dumps(groupByService)
    return JsonResponse({'data': data})
def tboardfiltercercle(req,*args, **kwargs):
    congeids = Conge.objects.filter(idpersonnel_field__organisme='Caida').values_list('idpersonnel_field', flat=True)
    listPerso = []
    for id in congeids:
        objj = Caidatpersonnel.objects.filter(idpersonnel_field=id).values('idpersonnel_field',
                                                                           'idcaidat_field__idcercle_field__libellecerclear',
                                                                           'idcaidat_field__idcercle_field__libellecerclefr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idcaidat_field__idcercle_field__libellecerclefr'] for d in listPerso])
    groupByDivision = []
    for key, value in dict(count).items():
        cercar = Cercle.objects.get(libellecerclefr=key)
        val = {'idcaidat_field__idcercle_field__libellecerclefr': key,
               'idcaidat_field__idcercle_field__libellecerclear': cercar.libellecerclear, 'dcount': value}
        groupByDivision.append(val)
    data = json.dumps(groupByDivision)
    return JsonResponse({'data': data})
def tboardfiltercaidat(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeids = Conge.objects.filter(idpersonnel_field__organisme='Caida').values_list('idpersonnel_field', flat=True)
    Qdiv = Q(idcaidat_field__idcercle_field__libellecerclefr=obj)
    '''groupByService = (Servicepersonnel.objects.filter(Qperso & Qdiv)
                      .values('idservice_field__libelleservicear', 'idservice_field__libelleservicefr')
                      .annotate(dcount=Count('idservice_field'))
                      .order_by()
                      )'''
    idscaida = Caidatpersonnel.objects.filter(Qdiv).values_list('idpersonnel_field', flat=True)
    listfinal = []
    for a in congeids:
        if a in idscaida:
            listfinal.append(a)
    listPerso = []
    for id in listfinal:
        Qid = Q(idpersonnel_field=id)
        objj = Caidatpersonnel.objects.filter(Qid & Qdiv).values('idpersonnel_field',
                                                                  'idcaidat_field__libellecaidatar',
                                                                  'idcaidat_field__libellecaidatfr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idcaidat_field__libellecaidatfr'] for d in listPerso])
    groupByCaidat = []
    for key, value in dict(count).items():
        caidaar = Caidat.objects.get(libellecaidatfr=key)
        val = {'idcaidat_field__libellecaidatfr': key,
               'idcaidat_field__libellecaidatar': caidaar.libellecaidatar, 'dcount': value}
        groupByCaidat.append(val)
    data = json.dumps(groupByCaidat)
    return JsonResponse({'data': data})
def tboardfilterpashalik(req,*args, **kwargs):
    congeids = Conge.objects.filter(idpersonnel_field__organisme='pashalik').values_list('idpersonnel_field', flat=True)
    listPerso = []
    for id in congeids:
        objj = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values('idpersonnel_field',
                                                                            'idpashalik_field__libellepashalikar',
                                                                            'idpashalik_field__libellepashalikfr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idpashalik_field__libellepashalikfr'] for d in listPerso])
    groupByPashalik = []
    for key, value in dict(count).items():
        pashar = Pashalik.objects.get(libellepashalikfr=key)
        val = {'idpashalik_field__libellepashalikfr': key,
               'idpashalik_field__libellepashalikar': pashar.libellepashalikar, 'dcount': value}
        groupByPashalik.append(val)
    data = json.dumps(groupByPashalik)
    return JsonResponse({'data': data})
def tboardfilterdistrict(req,*args, **kwargs):
    congeids = Conge.objects.filter(idpersonnel_field__organisme='Annexe').values_list('idpersonnel_field', flat=True)
    listPerso = []
    for id in congeids:
        objj = Annexepersonnel.objects.filter(idpersonnel_field=id).values('idpersonnel_field',
                                                                           'idannexe_field__iddistrict_field__libelledistrictar',
                                                                           'idannexe_field__iddistrict_field__libelledistrictfr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idannexe_field__iddistrict_field__libelledistrictfr'] for d in listPerso])
    groubByDistrict = []
    for key, value in dict(count).items():
        discar = District.objects.get(libelledistrictfr=key)
        val = {'idannexe_field__iddistrict_field__libelledistrictfr': key,
               'idannexe_field__iddistrict_field__libelledistrictar': discar.libelledistrictar, 'dcount': value}
        groubByDistrict.append(val)
    data = json.dumps(groubByDistrict)
    return JsonResponse({'data': data})
def tboardfilterannexe(req,*args, **kwargs):
    obj=kwargs.get('obj')
    print(obj)
    congeids = Conge.objects.filter(idpersonnel_field__organisme='Annexe').values_list('idpersonnel_field', flat=True)
    QAnnexe = Q(idannexe_field__iddistrict_field__libelledistrictfr=obj)
    idsAnnexe = Annexepersonnel.objects.filter(QAnnexe).values_list('idpersonnel_field', flat=True)
    listfinal = []
    print(idsAnnexe)
    for a in congeids:
        if a in idsAnnexe:
            listfinal.append(a)
    listPerso = []
    for id in listfinal:
        Qid = Q(idpersonnel_field=id)
        objj = Annexepersonnel.objects.filter(Qid & QAnnexe).values('idpersonnel_field',
                                                                 'idannexe_field__libelleannexear',
                                                                 'idannexe_field__libelleannexefr').first()
        listPerso.append(objj)
    count = collections.Counter([d['idannexe_field__libelleannexefr'] for d in listPerso])
    groubByAnnexe = []
    for key, value in dict(count).items():
        annexeAr = Annexe.objects.get(libelleannexefr=key)
        val = {'idannexe_field__libelleannexefr': key,
               'idannexe_field__libelleannexear': annexeAr.libelleannexear, 'dcount': value}
        groubByAnnexe.append(val)
    data = json.dumps(groubByAnnexe)
    print(data)
    return JsonResponse({'data': data})
def tboardajaxfilterpashaliktypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeCount = Conge.objects.filter(idpersonnel_field__organisme='pashalik').count()

    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='pashalik')).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='pashalik')).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='pashalik')).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='pashalik')).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='pashalik')).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    print(objdata)
    print(data)
    return JsonResponse({'data': data})
def tboardajaxfiltersecretariattypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeCount = Conge.objects.filter(idpersonnel_field__organisme='Service').count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='Service')).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Service')).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Service')).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Service')).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Service')).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdistricttypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeCount = Conge.objects.filter(idpersonnel_field__organisme='Annexe').count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='Annexe')).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Annexe')).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Annexe')).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Annexe')).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Annexe')).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfiltercercletypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeCount = Conge.objects.filter(idpersonnel_field__organisme='Caida').count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='Caida')).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Caida')).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Caida')).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Caida')).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Caida')).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterservicetypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Service') & Q(idservice_field__iddivision_field__libelledivisionfr=obj)).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdivisiontypeconge(req,*args, **kwargs):
    obj=kwargs.get('obj')
    divids=Servicepersonnel.objects.filter(idservice_field__iddivision_field__libelledivisionfr=obj).values_list('idpersonnel_field',flat=True)
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدراية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids)).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = (congeAdmiCount / congeCount) * 100
    congeMotCountPer = (congeMotCount / congeCount) * 100
    congeFatCountPer = (congeFatCount / congeCount) * 100
    congeHajCountPer = (congeHajCount / congeCount) * 100
    congeExpCountPer = (congeExpCount / congeCount) * 100
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})