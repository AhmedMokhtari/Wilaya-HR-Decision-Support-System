from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from GestionPersonnel.models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.db import connection
from datetime import date, datetime, timedelta
from django.db.models import Q,Sum
from .utils import *


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