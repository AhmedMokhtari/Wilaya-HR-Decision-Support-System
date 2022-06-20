from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from GestionPersonnel.models import *
import collections
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
    convertCongeToEnCour()
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

        return render(request, 'GestionConge/consultationconge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'objconge': objconge, 'conges': conges, 'divisions': divisions})
    return render(request, 'GestionConge/consultationconge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges,'divisions': divisions})


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
    convertCongeToEnCour()
    Q1 = Q(statut='جاري')
    Q2 = Q(dateretour__gt= datetime.now())
    congesEncour = Conge.objects.filter(Q1 & Q2)
    listdate =[]
    dateelimine = DateElimine.objects.all()
    for a in congesEncour:
        '''d1 = datetime.strptime(str(a.dateretour.strftime('%Y/%m/%d')), "%Y/%m/%d")
        d2 = datetime.strptime(str(date.today().strftime('%Y/%m/%d')), "%Y/%m/%d")
        delta = d1 - d2; delta.days'''
        datedecom = a.dateretour
        a2 = datetime.strptime(str(datedecom.strftime('%Y/%m/%d')), "%Y/%m/%d")
        a1 = datetime.now()
        data = [s.dateelimine.date() for s in dateelimine]
        datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
        b={'joursrestanConge':datenbjours}
        listdate.append(b);
    EncourFini=Conge.objects.filter(Q1 & Q(dateretour__lte=datetime.now()))
    congeScCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Q1).count()
    congePsCount = Conge.objects.filter(Q(idpersonnel_field__organisme='pashalik') & Q1).count()
    congeDsCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') & Q1).count()
    congeCrCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') & Q1).count()

    if(request.method=='POST'):
        id=request.POST.getlist('id[]')
        Conge.objects.filter(idconge__in=id).update(statut='انتهى')
    return render(request, 'GestionConge/congeEnCours.html', {'congesEnCours':zip(congesEncour,listdate),'enCoursFini':EncourFini,'congeScCount':congeScCount,
                                                              'congePsCount':congePsCount,'congeDsCount':congeDsCount,'congeCrCount':congeCrCount})


@login_required(login_url='/')
def congeconsultationfilter(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    etatconge = arr[0]
    if (etatconge != ''):
        statut = Q(statut=etatconge)
    else:
        statut = ~Q(idconge=None)  ## Always true0
    typeconge = arr[1]
    if (typeconge != ''):
        type_conge = Q(type_conge=typeconge)
    else:
        type_conge = ~Q(idconge=None)  ## Always true0
    conge = Conge.objects.filter(type_conge & statut).values('idpersonnel_field__nomar','idpersonnel_field__prenomar','type_conge','statut','datedebut__date','dateretour__date','nbjour')
    data = json.dumps(list(conge), default=str)
    return JsonResponse({'data': data})

@login_required(login_url='/')
def congeconsultationfilterdate(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('&')
    etatconge = arr[0]
    print(etatconge)
    print(vl)
    if (etatconge != ''):
        statut = Q(statut=etatconge)
    else:
        statut = ~Q(idconge=None)  ## Always true0
    typeconge = arr[1]
    if (typeconge != ''):
        type_conge = Q(type_conge=typeconge)
    else:
        type_conge = ~Q(idconge=None)  ## Always true0
    conge = Conge.objects.filter(type_conge & statut & Q(datedebut__gte=datetime.fromisoformat(arr[2])) & Q(dateretour__lte=datetime.fromisoformat(arr[3]) ) ).values('idpersonnel_field__nomar','idpersonnel_field__prenomar','type_conge','statut','datedebut__date','dateretour__date','nbjour')
    data = json.dumps(list(conge), default=str)
    return JsonResponse({'data': data})

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
    convertCongeToEnCour()
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
    convertCongeToEnCour()
    personnels = Personnel.objects.all()
    conges = Conge.objects.all()
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(
            Conge.objects.filter(datedebut__year=datetime.now().year).filter(datedebut__month=i + 1).count())
        i = i + 1
    print(congepersonnel)
    '''try:
        sql = "select d.LibelleDivisionAr,d.LibelleDivisionFr, count(c.IdConge) as total from [dbo].[Division] d inner join [dbo].[Service] s on s.IdDivision# = d.IdDivision inner join [dbo].[ServicePersonnel] sp on s.IdService = sp.IdService# inner join [dbo].[Personnel] p on sp.IdPersonnel# = p.IdPersonnel  inner join [dbo].[Conge] c on p.IdPersonnel = c.IdPersonnel# where p.organisme='Service' group by d.LibelleDivisionAr,d.LibelleDivisionFr,d.IdDivision"
        cursor = connection.cursor()
        cursor.execute(sql)
        divisions = list(cursor.fetchall())
    except Exception as e:
        exception = str(e)
    finally:
        cursor.close'''
    congeAdmiCount=Conge.objects.filter(type_conge='رخصة إدارية').count()
    congeExpCount=Conge.objects.filter(type_conge='رخصة استثنائية').count()
    congeHajCount=Conge.objects.filter(type_conge='رخصة الحج').count()
    congeMotCount=Conge.objects.filter(type_conge='رخصة الأموة').count()
    congeFatCount=Conge.objects.filter(type_conge='الرخصة الأبوية').count()

    congeScCount = Conge.objects.filter(idpersonnel_field__organisme='Service').count()
    congePsCount = Conge.objects.filter(idpersonnel_field__organisme='pashalik').count()
    congeDsCount = Conge.objects.filter(idpersonnel_field__organisme='Annexe').count()
    congeCrCount = Conge.objects.filter(idpersonnel_field__organisme='Caida').count()

    congeCount=Conge.objects.all().count()
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    congeHommeCount=Conge.objects.filter(idpersonnel_field__sexe='Homme-ذكر').count()
    congeFemmeCount=Conge.objects.filter(idpersonnel_field__sexe='Femme-أنثى').count()
    congeFemmeCountPer='{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer='{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount=Conge.objects.filter(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral').count()
    congeGeneralCount=Conge.objects.filter(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général').count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    context={'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges,'Sc':congeScCount,'Ps':congePsCount,'Cr':congeCrCount,'Ds':congeDsCount,
            'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount ,'congeFatCount':congeFatCount,
             'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeExpCountPer':congeExpCountPer,'congeHajCountPer':congeHajCountPer,
             'congeHommeCount':congeHommeCount,'congeFemmeCount':congeFemmeCount,'congeFemmeCountPer':congeFemmeCountPer,'congeHommeCountPer':congeHommeCountPer,
             'congePrefectoralCount':congePrefectoralCount,'congeGeneralCount':congeGeneralCount,'congeGeneralCountPer':congeGeneralCountPer,'congePrefectoralCountPer':congePrefectoralCountPer}
    return render (request,'GestionConge/tboardconges.html', context)

def tboardfilterdiv(req,*args, **kwargs):
    '''groupByDivision = (Servicepersonnel.objects.filter(idpersonnel_field__in=congeids)
                       .values('idservice_field__iddivision_field__libelledivisionar',
                               'idservice_field__iddivision_field__libelledivisionfr')
                       .annotate(dcount=Count('idservice_field__iddivision_field'))
                       .order_by()
                       )'''
    year = kwargs.get('obj')
    if (year != 'none'):
        if (year == 'encour'):
            Qyear = Q(statut='حاليا')
        else:
            Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeids=Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Qyear).values_list('idpersonnel_field',flat=True)
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
    data = json.dumps(groupByDivision)
    return JsonResponse({'data': data})
def tboardfilterdivse(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    congeids=Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Qyear).values_list('idpersonnel_field',flat=True)
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
    year = kwargs.get('obj')
    if (year != 'none'):
        if (year == 'encour'):
            Qyear = Q(statut='حاليا')
        else:
            Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeids = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') & Qyear).values_list('idpersonnel_field', flat=True)
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
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    congeids = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') & Qyear).values_list('idpersonnel_field', flat=True)
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
    year = kwargs.get('obj')
    if (year != 'none'):
        if (year == 'encour'):
            Qyear = Q(statut='حاليا')
        else:
            Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeids = Conge.objects.filter(Q(idpersonnel_field__organisme='pashalik') &Qyear).values_list('idpersonnel_field', flat=True)
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
    year = kwargs.get('obj')
    if (year != 'none'):
        if (year == 'encour'):
            Qyear = Q(statut='حاليا')
        else:
            Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeids = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') & Qyear).values_list('idpersonnel_field', flat=True)
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
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    congeids = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') & Qyear).values_list('idpersonnel_field', flat=True)
    QAnnexe = Q(idannexe_field__iddistrict_field__libelledistrictfr=obj)
    idsAnnexe = Annexepersonnel.objects.filter(QAnnexe).values_list('idpersonnel_field', flat=True)
    listfinal = []
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
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='pashalik') &Qyear).count()

    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer ='{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    print(objdata)
    print(data)
    return JsonResponse({'data': data})
def tboardajaxfiltersecretariattypeconge(req,*args, **kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Service') &Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdistricttypeconge(req,*args, **kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfiltercercletypeconge(req,*args, **kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdivisiontypeconge(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    divids=Servicepersonnel.objects.filter(idservice_field__iddivision_field__libelledivisionfr=obj).values_list('idpersonnel_field',flat=True)
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Service') & Q(idpersonnel_field__in=divids) &Qyear).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterannexetypeconge(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    divids=Annexepersonnel.objects.filter(idannexe_field__iddistrict_field__libelledistrictfr=obj).values_list('idpersonnel_field',flat=True)
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Annexe') & Q(idpersonnel_field__in=divids) &Qyear).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfiltercaidattypeconge(req,*args, **kwargs):
    vl=kwargs.get('obj')
    arr = vl.split('-')
    year=arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj=arr[0]
    divids=Caidatpersonnel.objects.filter(idcaidat_field__idcercle_field__libellecerclefr=obj).values_list('idpersonnel_field',flat=True)
    congeCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Q(idpersonnel_field__organisme='Caida') & Q(idpersonnel_field__in=divids) & Qyear).count()
    if(congeCount==0):
        congeCount=1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata={'congeAdmiCount':congeAdmiCount,'congeExpCount':congeExpCount,'congeHajCount':congeHajCount,'congeMotCount':congeMotCount,'congeFatCount':congeFatCount,
         'congeAdmiCountPer':congeAdmiCountPer,'congeMotCountPer':congeMotCountPer,'congeFatCountPer':congeFatCountPer,'congeHajCountPer':congeHajCountPer,'congeExpCountPer':congeExpCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterpashalikPer(req,*arg,**kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    Qpashalik=Q(idpersonnel_field__organisme='pashalik')
    congeCount = Conge.objects.filter(Qpashalik & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qpashalik  & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qpashalik & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral') & Qpashalik & Qyear ).count()
    congeGeneralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général') & Qpashalik & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount, 'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdivisionPer(req,*arg,**kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    Qpashalik = Q(idpersonnel_field__organisme='Service')
    congeCount = Conge.objects.filter(Qpashalik & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qpashalik & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qpashalik & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral') & Qpashalik & Qyear).count()
    congeGeneralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général') & Qpashalik & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfiltercaerclePer(req,*arg,**kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    Qpashalik = Q(idpersonnel_field__organisme='Caida')
    congeCount = Conge.objects.filter(Qpashalik & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qpashalik & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qpashalik & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral') & Qpashalik & Qyear).count()
    congeGeneralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général') & Qpashalik & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdistrictPer(req,*arg,**kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    QDistrict = Q(idpersonnel_field__organisme='Annexe')
    congeCount = Conge.objects.filter(QDistrict & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & QDistrict & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & QDistrict & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral') & QDistrict & Qyear).count()
    congeGeneralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général') & QDistrict & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterdivisionservPer(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    divids=Servicepersonnel.objects.filter(idservice_field__iddivision_field__libelledivisionfr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Service')
    Qdiv=Q(idpersonnel_field__in=divids)
    congeCount = Conge.objects.filter(Qdiv & Qorganisme & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfilterannexePer(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    divids=Annexepersonnel.objects.filter(idannexe_field__iddistrict_field__libelledistrictfr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Annexe')
    Qdiv=Q(idpersonnel_field__in=divids)
    congeCount = Conge.objects.filter(Qdiv & Qorganisme & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardajaxfiltercaidatPer(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    obj = arr[0]
    divids=Caidatpersonnel.objects.filter(idcaidat_field__idcercle_field__libellecerclefr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Caida')
    Qdiv=Q(idpersonnel_field__in=divids)
    congeCount = Conge.objects.filter(Qdiv & Qorganisme & Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى') & Qdiv & Qorganisme & Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCount = Conge.objects.filter(
        Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général')& Qdiv & Qorganisme & Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def tboardcongedefaultyear(req,*args, **kwargs):
    year = kwargs.get('obj')
    if(year!='none'):
        Qyear=Q(dateretour__year=year)
    else:
        Qyear=~Q(idconge=None) ## Always true0
    congeCount = Conge.objects.filter(Qyear).count()
    congeAdmiCount = Conge.objects.filter(Q(type_conge='رخصة إدارية') & Qyear).count()
    congeExpCount = Conge.objects.filter(Q(type_conge='رخصة استثنائية') & Qyear).count()
    congeHajCount = Conge.objects.filter(Q(type_conge='رخصة الحج') & Qyear).count()
    congeMotCount = Conge.objects.filter(Q(type_conge='رخصة الأموة') & Qyear).count()
    congeFatCount = Conge.objects.filter(Q(type_conge='الرخصة الأبوية') & Qyear).count()

    congeScCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Service') &Qyear).count()
    congePsCount = Conge.objects.filter(Q(idpersonnel_field__organisme='pashalik') &Qyear).count()
    congeDsCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Annexe') &Qyear).count()
    congeCrCount = Conge.objects.filter(Q(idpersonnel_field__organisme='Caida') &Qyear).count()
    if (congeCount == 0):
        congeCount = 1
    congeAdmiCountPer = '{:.2f}'.format((congeAdmiCount / congeCount) * 100)
    congeMotCountPer = '{:.2f}'.format((congeMotCount / congeCount) * 100)
    congeFatCountPer = '{:.2f}'.format((congeFatCount / congeCount) * 100)
    congeHajCountPer = '{:.2f}'.format((congeHajCount / congeCount) * 100)
    congeExpCountPer = '{:.2f}'.format((congeExpCount / congeCount) * 100)
    objdata = {'congeAdmiCount': congeAdmiCount, 'congeExpCount': congeExpCount, 'congeHajCount': congeHajCount,
               'congeMotCount': congeMotCount, 'congeFatCount': congeFatCount,
               'congeAdmiCountPer': congeAdmiCountPer, 'congeMotCountPer': congeMotCountPer,
               'congeFatCountPer': congeFatCountPer, 'congeHajCountPer': congeHajCountPer,
               'congeExpCountPer': congeExpCountPer,'congeCrCount':congeCrCount,'congeDsCount':congeDsCount,
               'congePsCount':congePsCount,'congeScCount':congeScCount}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})
def congencourfilter(req,*args, **kwargs):
    obj = kwargs.get('obj')
    conge=Conge.objects.filter(Q(idpersonnel_field__organisme=obj) & Q(statut='جاري') & Q(dateretour__gt= datetime.now())).values('idconge','idpersonnel_field__nomar',
                                                                                                                                   'idpersonnel_field__prenomar','type_conge','datedebut__date',
                                                                                                                                   'dateretour__date','nbjour')
    listdate = []
    dateelimine = DateElimine.objects.all()
    print(list(conge))
    for a in list(conge):
        print(a)
        '''d1 = datetime.strptime(str(a.dateretour.strftime('%Y/%m/%d')), "%Y/%m/%d")
        d2 = datetime.strptime(str(date.today().strftime('%Y/%m/%d')), "%Y/%m/%d")
        delta = d1 - d2; delta.days'''
        datedecom = a['dateretour__date']
        a2 = datetime.strptime(str(datedecom.strftime('%Y/%m/%d')), "%Y/%m/%d")
        a1 = datetime.now()
        data = [s.dateelimine.date() for s in dateelimine]
        datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
        b = {'idconge':a['idconge'],'idpersonnel_field__nomar':a['idpersonnel_field__nomar'],'idpersonnel_field__prenomar':a['idpersonnel_field__prenomar'],
            'type_conge':a['type_conge'],'datedebut__date':a['datedebut__date'],'dateretour__date':a['dateretour__date'],'nbjour':a['nbjour'],'joursrestanConge': datenbjours}
        listdate.append(b);
    data = json.dumps(listdate,default=str)
    return JsonResponse({'data': data},safe=False)
def congencourfinifilter(req,*args, **kwargs):
    obj = kwargs.get('obj')
    conge=Conge.objects.filter(Q(idpersonnel_field__organisme=obj) & Q(statut='جاري') & Q(dateretour__lte=datetime.now())).values('idconge','idpersonnel_field__nomar',
                                                                                                                                   'idpersonnel_field__prenomar','type_conge','datedebut__date',
                                                                                                                                   'dateretour__date','nbjour')
    datafini = json.dumps(list(conge),default=str)
    return JsonResponse({'datafini': datafini},safe=False)
def tboardajaxfilterentiteyear(req,*arg,**kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    orgnisme = arr[0]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = Q(datedebut__year=datetime.now().year)
    Qorganisme=Q(idpersonnel_field__organisme=orgnisme)

    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(Qyear & Q(datedebut__month=i + 1) & Qorganisme).count())
        i = i + 1
    data = json.dumps(congepersonnel)
    return JsonResponse({'data': data})

def tboardajaxfilterserviceyear(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = Q(datedebut__year=datetime.now().year)
    obj = arr[0]
    divids=Servicepersonnel.objects.filter(idservice_field__iddivision_field__libelledivisionfr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Service')
    Qdiv=Q(idpersonnel_field__in=divids)
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(Qyear & Q(datedebut__month=i + 1) & Qorganisme & Qdiv).count())
        i = i + 1
    data = json.dumps(congepersonnel)
    return JsonResponse({'data': data})
def tboardajaxfilterannexeyear(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = Q(datedebut__year=datetime.now().year)
    obj = arr[0]
    divids=Annexepersonnel.objects.filter(idannexe_field__iddistrict_field__libelledistrictfr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Annexe')
    Qdiv=Q(idpersonnel_field__in=divids)
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(Qyear & Q(datedebut__month=i + 1) & Qorganisme & Qdiv).count())
        i = i + 1
    data = json.dumps(congepersonnel)
    return JsonResponse({'data': data})
def tboardajaxfiltercaidatyear(req,*args, **kwargs):
    vl = kwargs.get('obj')
    arr = vl.split('-')
    year = arr[1]
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = Q(datedebut__year=datetime.now().year)
    obj = arr[0]
    divids=Caidatpersonnel.objects.filter(idcaidat_field__idcercle_field__libellecerclefr=obj).values_list('idpersonnel_field',flat=True)
    Qorganisme=Q(idpersonnel_field__organisme='Caida')
    Qdiv=Q(idpersonnel_field__in=divids)
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(Qyear & Q(datedebut__month=i + 1) & Qorganisme & Qdiv).count())
        i = i + 1
    data = json.dumps(congepersonnel)
    return JsonResponse({'data': data})
def tboardcongedefaultyearchart(req,*arg,**kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = Q(datedebut__year=datetime.now().year)
    congepersonnel = []
    i = 0
    while i <= 11:
        congepersonnel.append(Conge.objects.filter(Qyear & Q(datedebut__month=i + 1)).count())
        i = i + 1
    data = json.dumps(congepersonnel)
    return JsonResponse({'data': data})
def tboardajaxfilteryeardefault(req,*args, **kwargs):
    year = kwargs.get('obj')
    if (year != 'none'):
        Qyear = Q(dateretour__year=year)
    else:
        Qyear = ~Q(idconge=None)  ## Always true0
    congeCount=Conge.objects.filter(Qyear).count()
    if(congeCount==0):
        congeCount=1
    congeHommeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Homme-ذكر')& Qyear).count()
    congeFemmeCount = Conge.objects.filter(Q(idpersonnel_field__sexe='Femme-أنثى')& Qyear).count()
    congeFemmeCountPer = '{:.2f}'.format((congeFemmeCount / congeCount) * 100)
    congeHommeCountPer = '{:.2f}'.format((congeHommeCount / congeCount) * 100)
    congePrefectoralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral') & Qyear).count()
    congeGeneralCount = Conge.objects.filter(Q(idpersonnel_field__administrationapp='عمالة وجدة أنجاد-Général')& Qyear).count()
    congeGeneralCountPer = '{:.2f}'.format((congeGeneralCount / congeCount) * 100)
    congePrefectoralCountPer = '{:.2f}'.format((congePrefectoralCount / congeCount) * 100)
    objdata = {'congeHommeCount': congeHommeCount, 'congeFemmeCount': congeFemmeCount,
               'congeFemmeCountPer': congeFemmeCountPer,
               'congeHommeCountPer': congeHommeCountPer, 'congePrefectoralCount': congePrefectoralCount,
               'congeGeneralCount': congeGeneralCount, 'congeGeneralCountPer': congeGeneralCountPer,
               'congePrefectoralCountPer': congePrefectoralCountPer}
    data = json.dumps(objdata)
    return JsonResponse({'data': data})