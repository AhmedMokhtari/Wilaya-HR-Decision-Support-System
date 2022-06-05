from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
from django.http import HttpResponse, JsonResponse
import os
import datetime
import csv
import pandas as pd
import seaborn as sns
from .utils import calculate_age, get_graph, count_age_int, dictfetchall, dateRetraiteCalc
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.db import connection
import arabic_reshaper
from bidi.algorithm import get_display
from pathlib import Path
from operator import itemgetter


#personnel -------------------------------.
@login_required(login_url='/connexion')
def consultation(request):
    cursor = connection.cursor()
    cursor.execute('''with t1 as(select IdService#,IdPersonnel#,DateAffectation, ROW_NUMBER()  OVER ( PARTITION BY IdPersonnel# ORDER BY IdPersonnel#,DateAffectation desc ) RowNumber from ServicePersonnel )
    ,
    t2 as(
    select IdGrade#,IdPersonnel#,DateGrade, ROW_NUMBER()  OVER ( PARTITION BY IdPersonnel# ORDER BY IdPersonnel#,DateGrade desc ) RowNumber from GradePersonnel
    )
    select P.IdPersonnel,P.Sexe,P.Ppr, P.NomFr , P.PrenomFr,P.Cin,D.LibelleDivisionFr, S.LibelleServiceFr ,P.AdministrationApp ,t1.IdService#,t1.DateAffectation,t2.IdGrade#,t2.DateGrade,G.GradeFr
    from t1,t2 ,Service S ,Personnel P,Division D,Grade G where   t1.IdPersonnel# = t2.IdPersonnel#  and  t1.RowNumber = t2.RowNumber  and
    t1.RowNumber=1 AND S.IdService=t1.IdService# AND P.IdPersonnel=t1.IdPersonnel# AND D.IdDivision=S.IdDivision# AND G.IdGrade=t2.IdGrade#''')
    rows = dictfetchall(cursor)
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
        ## b = {'anneesum': Conge.objects.filter(Q1 & Q2).aggregate(Sum('nbjour'))}
        a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel','cin','ppr','nomfr','prenomfr','administrationapp','sexe','organisme','photo').first()
        b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                                 'idgrade_field__idstatutgrade_field__statutgradefr').last()
        c={};
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

        res={**a, **b,**c};
        listPerso.append(res)

    gradeperso = Gradepersonnel.objects.order_by('idpersonnel_field').values('idpersonnel_field','idpersonnel_field__cin','idpersonnel_field__ppr','idpersonnel_field__nomfr','idpersonnel_field__prenomfr','idpersonnel_field__administrationapp','idpersonnel_field__sexe','idpersonnel_field__organisme','idgrade_field__gradefr','idgrade_field__idstatutgrade_field__statutgradefr')

    return render(request, 'GestionPersonnel/consultation.html', {'personnels': rows, 'divsions': divisions,
                                                                  'grades': grades, 'gradeperso': gradeperso,
                                                                  'listPerso': listPerso, 'entites': entites,
                                                                  'pashaliks': pashaliks, 'districts':districts,
                                                                  'statutgrades': statutgrades, 'cercles': cercles})

#personnel information images -------------------------------.
def persoinfoimg(request) :
    division = Division.objects.all();
    grade = Grade.objects.all();
    personnels = { 'divs': division, 'grades': grade}
    return render(request, 'GestionPersonnel/persoinfoimg.html',personnels)

# filter -------------------------------.
@login_required(login_url='/connexion')
def get_json_perso_data(request, *args, **kwargs):
    selected_obj = kwargs.get('obj')
    arr=selected_obj.split("-");
    listPerso = []
    if(arr[0]=='entite'):
        if(arr[1]=='Secrétariat général'):
               perso = Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
               for id in perso:
                   a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                       'administrationapp', 'sexe', 'organisme',
                                                                       'photo').first()
                   b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                                  'idgrade_field__idstatutgrade_field__statutgradefr').last()
                   c = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                               'idservice_field__libelleservicear',
                               'idservice_field__libelleservicefr',
                               'idservice_field__iddivision_field__libelledivisionfr',
                               'idservice_field__iddivision_field__libelledivisionar').last()
                   if (not b):
                       b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                   if (not c):
                       c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                            'idservice_field__iddivision_field__libelledivisionar': ''}

                   res = {**a, **b, **c};
                   listPerso.append(res)
        elif(arr[1]=='Commandement'):
            persoPashalik = Personnel.objects.filter(organisme='pashalik').values_list('idpersonnel', flat=True)
            persoCaida = Personnel.objects.filter(organisme='Caida').values_list('idpersonnel', flat=True)
            persoAnnexe = Personnel.objects.filter(organisme='Annexe').values_list('idpersonnel', flat=True)
            for id in persoPashalik:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                    'idpashalik_field__libellepashalikfr',
                    'idpashalik_field__libellepashalikar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idpashalik_field__libellepashalikar': '', 'idpashalik_field__libellepashalikfr': '',}

                res = {**a, **b, **c};
                listPerso.append(res)
            for id in persoCaida:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                    'idcaidat_field__libellecaidatfr',
                    'idcaidat_field__libellecaidatar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idcaidat_field__libellecaidatar': '', 'idcaidat_field__libellecaidatfr': '',}

                res = {**a, **b, **c};
                listPerso.append(res)
            for id in persoAnnexe:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idannexe_field__libelleannexefr',
                    'idannexe_field__libelleannexear').last()
                print(c);
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idannexe_field__libelleannexear': '', 'idannexe_field__libelleannexefr  ': '',}

                res = {**a, **b, **c};
                listPerso.append(res)
        elif (arr[1] == 'Cabinet'):
            ServicePer = Servicepersonnel.objects.all();
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x);
            CabinetId = Division.objects.get(libelledivisionfr='Cabinet');
            servCabinet = Service.objects.filter(iddivision_field=CabinetId).values_list('idservice', flat=True);
            idServ = [user for user in PersoService if user['idservice_field'] in servCabinet]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            listidperso = Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it);
            for id in listfinal:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr',
                                                             'prenomfr',
                                                             'administrationapp', 'sexe', 'organisme',
                                                             'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                Q3 = Q(idpersonnel_field=id)
                Q4 = Q(idservice_field__in=servCabinet)
                c = Servicepersonnel.objects.filter(Q3 & Q4).values(
                    'idservice_field__libelleservicear',
                    'idservice_field__libelleservicefr',
                    'idservice_field__iddivision_field__libelledivisionfr',
                    'idservice_field__iddivision_field__libelledivisionar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                         'idservice_field__iddivision_field__libelledivisionar': ''}

                res = {**a, **b, **c};
                listPerso.append(res)
        elif (arr[1] == 'Dai'):
            ServicePer = Servicepersonnel.objects.all();
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x);
            daiId = Division.objects.get(libelledivisionfr='Dai');
            servDai = Service.objects.filter(iddivision_field=daiId).values_list('idservice', flat=True);
            idServ = [user for user in PersoService if user['idservice_field'] in servDai]
            listofid = []
            for a in idServ:
                listofid.append(a['idpersonnel_field'])
            listidperso = Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
            listfinal = []
            for it in listidperso:
                if it in listofid:
                    listfinal.append(it);
            for id in listfinal:
                Q1 = Q(idpersonnel=id)
                a = Personnel.objects.filter(Q1 & Q2).values('idpersonnel', 'cin', 'ppr', 'nomfr',
                                                             'prenomfr',
                                                             'administrationapp', 'sexe', 'organisme',
                                                             'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                Q3 = Q(idpersonnel_field=id)
                Q4 = Q(idservice_field__in=servDai)
                c = Servicepersonnel.objects.filter(Q3 & Q4).values(
                    'idservice_field__libelleservicear',
                    'idservice_field__libelleservicefr',
                    'idservice_field__iddivision_field__libelledivisionfr',
                    'idservice_field__iddivision_field__libelledivisionar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                         'idservice_field__iddivision_field__libelledivisionar': ''}

                res = {**a, **b, **c};
                listPerso.append(res)
        elif (arr[1] == 'Dsic'):
            ServicePer=Servicepersonnel.objects.all();
            servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
            PersoService = []
            for id in servid:
                x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idservice_field',
                    'idpersonnel_field').last()
                PersoService.append(x);
            DsicId= Division.objects.get(libelledivisionfr='DSIC');
            servDsic=Service.objects.filter(iddivision_field=DsicId).values_list('idservice', flat=True);
            superplayers = [user for user in PersoService if user['idservice_field'] in servDsic]
            listofid=[]
            for a in superplayers:
                listofid.append(a['idpersonnel_field'])
            listidperso=Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
            listfinal=[]
            for it in  listidperso:
                if it in listofid:
                    listfinal.append(it);
            for id in listfinal:
                Q1 = Q(idpersonnel=id)
                a = Personnel.objects.filter(Q1).values('idpersonnel', 'cin', 'ppr', 'nomfr',
                                                             'prenomfr',
                                                             'administrationapp', 'sexe', 'organisme',
                                                             'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                Q3 = Q(idpersonnel_field=id)
                Q4 = Q(idservice_field__in=servDsic)
                c = Servicepersonnel.objects.filter(Q3 & Q4).values(
                    'idservice_field__libelleservicear',
                    'idservice_field__libelleservicefr',
                    'idservice_field__iddivision_field__libelledivisionfr',
                    'idservice_field__iddivision_field__libelledivisionar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                         'idservice_field__iddivision_field__libelledivisionar': ''}

                res = {**a, **b, **c};
                listPerso.append(res)
    elif(arr[0]=='division'):
        ServicePer = Servicepersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        serv = Service.objects.filter(iddivision_field=arr[1]).values_list('idservice', flat=True);
        superplayers = [user for user in PersoService if user['idservice_field'] in serv]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        listidperso = Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr',
                                                         'prenomfr',
                                                         'administrationapp', 'sexe', 'organisme',
                                                         'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            Q3 = Q(idpersonnel_field=id)
            Q4 = Q(idservice_field__in=serv)
            c = Servicepersonnel.objects.filter(Q3 & Q4).values(
                'idservice_field__libelleservicear',
                'idservice_field__libelleservicefr',
                'idservice_field__iddivision_field__libelledivisionfr',
                'idservice_field__iddivision_field__libelledivisionar').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                     'idservice_field__iddivision_field__libelledivisionar': ''}

            res = {**a, **b, **c};
            listPerso.append(res)
    elif (arr[0] == 'service'):
        ServicePer = Servicepersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Servicepersonnel.objects.filter(idpersonnel_field=id).values(
                'idservice_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        superplayers = [user for user in PersoService if user['idservice_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        listidperso = Personnel.objects.filter(organisme='Service').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr',
                                                         'prenomfr',
                                                         'administrationapp', 'sexe', 'organisme',
                                                         'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            Q3 = Q(idpersonnel_field=id)
            Q4 = Q(idservice_field=arr[1])
            c = Servicepersonnel.objects.filter(Q3 & Q4).values(
                'idservice_field__libelleservicear',
                'idservice_field__libelleservicefr',
                'idservice_field__iddivision_field__libelledivisionfr',
                'idservice_field__iddivision_field__libelledivisionar').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idservice_field__libelleservicear': '', 'idservice_field__libelleservicefr': '',
                     'idservice_field__iddivision_field__libelledivisionar': ''}

            res = {**a, **b, **c};
            listPerso.append(res)
    elif (arr[0] == 'districtpashalik'):
        if(arr[1]=='Pashalik'):
            persoPashalik = Personnel.objects.filter(organisme='pashalik').values_list('idpersonnel', flat=True)
            for id in persoPashalik:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                    'idpashalik_field__libellepashalikfr',
                    'idpashalik_field__libellepashalikar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idpashalik_field__libellepashalikar': '', 'idpashalik_field__libellepashalikfr': '', }

                res = {**a, **b, **c};
                listPerso.append(res)
        elif(arr[1]=='Cercle'):
            persoCaida = Personnel.objects.filter(organisme='Caida').values_list('idpersonnel', flat=True)
            for id in persoCaida:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                    'idcaidat_field__libellecaidatfr',
                    'idcaidat_field__libellecaidatar').last()
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idcaidat_field__libellecaidatar': '', 'idcaidat_field__libellecaidatfr': '', }

                res = {**a, **b, **c};
                listPerso.append(res)
        elif(arr[1]=='District'):
            persoAnnexe = Personnel.objects.filter(organisme='Annexe').values_list('idpersonnel', flat=True)
            for id in persoAnnexe:
                a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                    'administrationapp', 'sexe', 'organisme',
                                                                    'photo').first()
                b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                               'idgrade_field__idstatutgrade_field__statutgradefr').last()
                c = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                    'idannexe_field__libelleannexefr',
                    'idannexe_field__libelleannexear').last()
                print(c);
                if (not b):
                    b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
                if (not c):
                    c = {'idannexe_field__libelleannexear': '', 'idannexe_field__libelleannexefr  ': '', }

                res = {**a, **b, **c};
                listPerso.append(res)
    elif (arr[0] == 'district'):
        ServicePer = Annexepersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        servAnnex = Annexe.objects.filter(iddistrict_field=arr[1]).values_list('idannexe',flat=True);
        superplayers = [user for user in PersoService if user['idannexe_field'] in servAnnex]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        annexid = Annexe.objects.filter(iddistrict_field=arr[1]).values_list('idannexe')
        listidperso = Personnel.objects.filter(organisme='Annexe').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        print(listfinal)
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                'administrationapp', 'sexe', 'organisme',
                                                                'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            Q1 = Q(idpersonnel_field=id);
            Q2=Q(idannexe_field__in=annexid);
            c = Annexepersonnel.objects.filter(Q1 & Q2).values(
                'idannexe_field__libelleannexefr',
                'idannexe_field__libelleannexear').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idannexe_field__libelleannexear': '', 'idannexe_field__libelleannexefr  ': '', }

            res = {**a, **b, **c};
            listPerso.append(res)
    elif (arr[0] == 'cercle'):
        ServicePer = Caidatpersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Caidatpersonnel.objects.filter(idpersonnel_field=id).values(
                'idcaidat_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        servCaida = Caidat.objects.filter(idcercle_field=arr[1]).values_list('idcaidat',flat=True);
        superplayers = [user for user in PersoService if user['idcaidat_field'] in servCaida]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        caidatid = Caidat.objects.filter(idcercle_field=arr[1]).values_list('idcaidat')
        listidperso = Personnel.objects.filter(organisme='Caida').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        print(listfinal)
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                'administrationapp', 'sexe', 'organisme',
                                                                'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            Q1 = Q(idpersonnel_field=id);
            Q2=Q(idcaidat_field__in=caidatid);
            c = Caidatpersonnel.objects.filter(Q1 & Q2).values(
                'idcaidat_field__libellecaidatar',
                'idcaidat_field__libellecaidatfr').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idcaidat_field__libellecaidatar': '', 'idcaidat_field__libellecaidatfr': '', }

            res = {**a, **b, **c};
            listPerso.append(res)
    elif (arr[0] == 'annexe'):
        ServicePer = Annexepersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        superplayers = [user for user in PersoService if user['idannexe_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        listidperso = Personnel.objects.filter(organisme='Annexe').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        print(listfinal)
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                'administrationapp', 'sexe', 'organisme',
                                                                'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            c = Annexepersonnel.objects.filter(idpersonnel_field=id).values(
                'idannexe_field__libelleannexefr',
                'idannexe_field__libelleannexear').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idannexe_field__libelleannexear': '', 'idannexe_field__libelleannexefr  ': '', }
            res = {**a, **b, **c};
            listPerso.append(res)
    elif (arr[0] == 'pashalik'):
        ServicePer = Pashalikpersonnel.objects.all();
        servid = ServicePer.order_by('idpersonnel_field').values_list('idpersonnel_field', flat=True).distinct()
        PersoService = []
        for id in servid:
            x = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                'idpashalik_field',
                'idpersonnel_field').last()
            PersoService.append(x);
        superplayers = [user for user in PersoService if user['idpashalik_field'] == int(arr[1])]
        listofid = []
        for a in superplayers:
            listofid.append(a['idpersonnel_field'])
        listidperso = Personnel.objects.filter(organisme='pashalik').values_list('idpersonnel', flat=True)
        listfinal = []
        for it in listidperso:
            if it in listofid:
                listfinal.append(it);
        print(listfinal)
        for id in listfinal:
            a = Personnel.objects.filter(idpersonnel=id).values('idpersonnel', 'cin', 'ppr', 'nomfr', 'prenomfr',
                                                                'administrationapp', 'sexe', 'organisme',
                                                                'photo').first()
            b = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                           'idgrade_field__idstatutgrade_field__statutgradefr').last()
            c = Pashalikpersonnel.objects.filter(idpersonnel_field=id).values(
                'idpashalik_field__libellepashalikfr',
                'idpashalik_field__libellepashalikar').last()
            if (not b):
                b = {'idgrade_field__gradefr': '', 'idgrade_field__idstatutgrade_field__statutgradefr': ''}
            if (not c):
                c = {'idpashalik_field__libellepashalikfr': '', 'idpashalik_field__libellepashalikar  ': '', }
            res = {**a, **b, **c};
            listPerso.append(res)
    ##data = serializers.serialize("json",listPerso )
    data=json.dumps(listPerso)
    return JsonResponse({'data': data})

#export-------------------------------
def export_perso_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="personnels.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['CIN', 'NOM', 'PRENOM', 'LIEU DE NAISSENCE', 'EMAIL', 'TEL ', 'SITUATION FAMILIALER'])
    personnels = Personnel.objects.all().values_list('cin', 'nomfr', 'prenomfr', 'lieunaissancefr', 'email', 'tele', 'situationfamilialefr')
    for personnel in personnels:
        writer.writerow(personnel)
    return response

#info -------------------------------.
def info(request,id):
    personnel = Personnel.objects.get(idpersonnel=id)
    conjointsinperso = Conjointpersonnel.objects.filter(idpersonnel_field=id)
    conjoints = Conjoint.objects.filter(idconjoint__in=conjointsinperso.values_list('idconjoint_field', flat=True))
    serviperso = Servicepersonnel.objects.filter(idpersonnel_field=id)
    Servii = Servicepersonnel.objects.filter(idpersonnel_field=id)
    Services = Service.objects.filter(idservice__in=Servii.values_list('idservice_field', flat=True))
    enfants = Enfant.objects.filter(idconjoint_field__in=conjointsinperso.values_list('idconjoint_field', flat=True))
    diplomes = Diplome.objects.filter(idpersonnel_field=id)
    return render(request, 'GestionPersonnel/info.html', {'personnel': personnel, 'conjoints': conjoints, 'conjointsinperso': conjointsinperso,
                                                          'Serviii': zip(Services, serviperso), 'diplomes':diplomes, "enfants":enfants})

def testfilter(request):
    services = Service.objects.all()
    grades = Grade.objects.all()
    fonctions = Fonction.objects.all()
    echellons = Echellon.objects.all()
    statutgrades = Statutgrade.objects.all()
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()
    return render(request, 'GestionPersonnel/test.html',
                  {'services': services, 'grades': grades, 'fonctions': fonctions,
                   'echellons': echellons, 'statutgrades': statutgrades,
                   'entites': entites, 'pashaliks': pashaliks,
                   'districts': districts, 'divisions': divisions, 'cercles': cercles})

def personnelinfo(request,id):
    grades = Gradepersonnel.objects.filter(idpersonnel_field=id).values('idgrade_field__gradefr',
                                                                        'idgrade_field__gradear',
                                                                        'idgrade_field__idstatutgrade_field__statutgradefr',
                                                                        'idechellon_field__echellon',
                                                                        'indice',
                                                                        'dateechellon',
                                                                        'changementdechellon',)
    fonctions = Fonctionpersonnel.objects.filter(idpersonnel_field=id).values('idfonction_field__libellefontionar',
                                                                        'idfonction_field__libellefonctionfr',
                                                                        'datefonction')
    conjoints= Conjointpersonnel.objects.filter(idpersonnel_field=id).values('idconjoint_field__cin',
                                                                        'idconjoint_field__nomar',
                                                                        'idconjoint_field__nomfr',
                                                                        'idconjoint_field__prenomar',
                                                                        'idconjoint_field__prenomfr',
                                                                        'idconjoint_field__datenaissance',
                                                                        'idconjoint_field__lieunaissance',
                                                                        'idconjoint_field__ppr',
                                                                        )
    conjointid=Conjointpersonnel.objects.filter(idpersonnel_field=id).values('idconjoint_field')
    enfants = Enfant.objects.filter(idconjoint_field__in=conjointid).values('nomar',
                                                                 'nomfr',
                                                                 'prenomfr',
                                                                 'prenomar',
                                                                 'datenaissance',
                                                                 'lieunaissancear',
                                                                 'lieunaissancefr',
                                                                 'idconjoint_field__cin',
                                                                 'idconjoint_field__nomar',
                                                                 'idconjoint_field__nomfr',
                                                                  'idconjoint_field__prenomar',
                                                                  'idconjoint_field__prenomfr',
                                                                  'idconjoint_field__datenaissance',
                                                                  'idconjoint_field__lieunaissance',
                                                                  'idconjoint_field__ppr',
                                                                              )
    diploms = Diplome.objects.filter(idpersonnel_field=id).values('diplomefr',
                                                                        'diplomear',
                                                                        'etablissement',
                                                                        'specialitear',
                                                                        'specialitefr',
                                                                        'datediplome')
    listobj=[]
    Service = Servicepersonnel.objects.filter(idpersonnel_field=id)
    for a in Service:
        obj={'libelleservicear':a.idservice_field.libelleservicear,
             'libelleservicefr':a.idservice_field.libelleservicefr,
             'libelledivisionar':a.idservice_field.iddivision_field.libelledivisionar,
             'libelledivisionfr': a.idservice_field.iddivision_field.libelledivisionfr,
             'dateaffectation':a.dateaffectation}
        listobj.append(obj);
    pashaliks = Pashalikpersonnel.objects.filter(idpersonnel_field=id)
    for a in pashaliks:
        obj={'libelleservicear':a.idpashalik_field.libellepashalikar,
             'libelleservicefr':a.idpashalik_field.libellepashalikfr,
             'libelledivisionar':"باشوية",
             'libelledivisionfr': "pashalik",
             'dateaffectation':a.dateaffectation}
        listobj.append(obj);
    Annexe = Annexepersonnel.objects.filter(idpersonnel_field=id)
    for a in Annexe:
        obj={'libelleservicear':a.idannexe_field.libelleannexear,
             'libelleservicefr':a.idannexe_field.libelleannexefr,
             'libelledivisionar':a.idannexe_field.iddistrict_field.libelledistrictar,
             'libelledivisionfr': a.idannexe_field.iddistrict_field.libelledistrictfr,
             'dateaffectation':a.dateaffectation}
        listobj.append(obj);
    caidat=Caidatpersonnel.objects.filter(idpersonnel_field=id)
    for a in caidat:
        obj={'libelleservicear':a.idcaidat_field.libellecaidatar,
             'libelleservicefr':a.idcaidat_field.libellecaidatfr,
             'libelledivisionar':a.idcaidat_field.idcercle_field.libellecerclear,
             'libelledivisionfr': a.idcaidat_field.idcercle_field.libellecerclefr,
             'dateaffectation':a.dateaffectation}
        listobj.append(obj);
    newlistsorted = sorted(listobj, key=itemgetter('dateaffectation'),reverse=True)
    persoinfo=Personnel.objects.get(idpersonnel=id);
    statuts=Statutpersonnel.objects.filter(idpersonnel_field=id);
    return render(request, 'GestionPersonnel/personnelinfo.html',
                  {'services': newlistsorted, 'grades': grades, 'fonctions': fonctions,
                   'conjoints': conjoints, 'enfants': enfants,'statuts':statuts,
                   'pashaliks': pashaliks,'diploms': diploms,'persoinfo':persoinfo})


# ajouter -------------------------------.
@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloaddivision(request):
    entite = Entite.objects.get(libelleentitefr=request.POST['entite'])
    objdivision = {"divisions": list(Division.objects.filter(identite_field=entite).values('iddivision','libelledivisionar','libelledivisionfr'))}
    return JsonResponse(objdivision, safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloadcaida(request):
    cercle = Cercle.objects.get(idcercle=request.POST.get('cercle', None))
    objcaida = {"caidas": list(Caidat.objects.filter(idcercle_field=cercle).values('idcaidat','libellecaidatar','libellecaidatfr'))}
    return JsonResponse(objcaida, safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloadsevice(request):
    division = Division.objects.get(iddivision=request.POST.get('division', None))
    objservice = {"services": list(Service.objects.filter(iddivision_field=division).values('idservice','libelleservicear','libelleservicefr'))}
    return JsonResponse(objservice, safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloadannexe(request):
    district = District.objects.get(iddistrict=request.POST.get('district', None))
    objannexe = {"annexes": list(Annexe.objects.filter(iddistrict_field=district).values('idannexe','libelleannexear','libelleannexefr'))}
    return JsonResponse(objannexe, safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloadgrade(request):
    statutgrade = Statutgrade.objects.get(idstatutgrade=request.POST.get('statutgrade', None))
    objstatutgrade = {"grades": list(Grade.objects.filter(idstatutgrade_field=statutgrade).values('idgrade','gradear','gradefr'))}
    return JsonResponse(objstatutgrade,safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxajouterloadechellon(request):

    statutgrade = Statutgrade.objects.get(idstatutgrade=request.POST.get('statutgrade', None))
    objgrade =Grade.objects.get(idgrade=request.POST.get('grade', None))
    grade = Grade.objects.filter(idstatutgrade_field=statutgrade).filter(idgrade=objgrade.idgrade).first()
    echellon = []
    indice = []
    if(statutgrade.statutgradefr == 'Administrateurs MI'):
        if(grade.idechelle_field.echelle == '10'):
            indice = ['275', '300', '329', '355', '380','402','428','460','484','512','564']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'EXP']
        elif (grade.idechelle_field.echelle == '11'):
            indice = ['336', '369', '406', '436', '476', '509', '542', '578', '610', '639','704']
            echellon = ['1','2','3','4','5','6','7','8','9','10','EXP']
        else:
            indice = ['704', '746', '779', '812', '840', '870']
            echellon = ['1', '2', '3', '4', '5', '6']
    elif(statutgrade.statutgradefr == 'Administrateurs AC'):
        if (grade.idechelle_field.echelle == '10'):
            indice = ['275', '300', '326', '351', '377', '402', '428', '456', '484', '512', '564']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'EXP']
        elif (grade.idechelle_field.echelle == '11'):
            indice = ['336', '369', '403', '436', '472', '509', '542', '574', '606', '639', '704']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'EXP']
        else:
            indice = ['704', '746', '779', '812', '840', '870']
            echellon = ['1', '2', '3', '4', '5', '6']
    elif(statutgrade.statutgradefr == "Ingénieurs et Architectes"):
        if(grade.gradefr == "Ingénieur d'Etat 1er grade"  or grade.gradefr == "Architecte 1er grade" ):
            indice = ['336','369','403','436','472']
            echellon = ['1', '2', '3', '4', '5']
        elif(grade.gradefr == "Ingénieur d'application 1er grade"):
            indice = ['275', '300', '326', '351', '377']
            echellon = ['1', '2', '3', '4', '5']
        elif(grade.gradefr == "Architecte en chef grade principal" or grade.gradefr == "Ingénieur d'Etat grade principal" ):
            indice = ['870', '900', '930', '960', '990']
            echellon = ['1', '2', '3', '4', '5']
        elif(grade.gradefr=="Ingénieur d'Etat grade principal" or grade.gradefr == "Architecte grade principal"):
            indice = ['509', '542', '574', '606', '639', '704']
            echellon = ['1', '2', '3', '4', '5', '6']
        elif(grade.gradefr == "Ingénieur en chef 1er grade" or grade.gradefr == "Architecte en chef 1er grade"):
            indice = ['704', '746', '779', '812', '840', '870']
            echellon = ['1', '2', '3', '4', '5', '6']
        elif(grade.gradefr == "Ingénieur d'application grade principal"):
            indice = ['402', '428', '456', '484', '512', '564']
            echellon = ['1', '2', '3', '4', '5', '6']
    elif(statutgrade.statutgradefr=="Techniciens" or statutgrade.statutgradefr=="Rédacteurs"):
        if(grade.idechelle_field.echelle == "8"):
            indice = ['207', '224', '241', '259', '276', '293', '311', '332', '353', '373']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        elif(grade.idechelle_field.echelle == "9"):
            indice = ['235', '253', '274', '296', '317', '339', '361', '382', '404', '438']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        elif(grade.idechelle_field.echelle == "10"):
            indice = ['275', '300', '326', '351', '377', '402', '428', '456', '484', '512', '564']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        elif (grade.idechelle_field.echelle == "11"):
            indice = ['336','369','403','436','472', '509', '542', '574', '606', '639', '675', '704', '690', '704']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    elif (statutgrade.statutgradefr == "Adjoints Administratifs" or statutgrade.statutgradefr == "Adjoints Techniques"):
        if (grade.idechelle_field.echelle == "8"):
            indice = ['207', '224', '241', '259', '276', '293', '311', '332', '353', '373']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        elif (grade.idechelle_field.echelle == "7"):
            indice = ['177', '193', '208', '225', '242', '260', '277', '291', '305', '318']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        elif (grade.idechelle_field.echelle == "6"):
            indice = ['153', '161', '173', '185', '197', '209', '222', '236', '249', '262']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        elif (grade.idechelle_field.echelle == "5"):
            indice = ['137', '141', '150', '157', '165', '174', '183', '192', '201', '220']
            echellon = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    data = {'echellon': echellon, 'indice': indice}
    return JsonResponse(data, safe=False)

@login_required(login_url='/connexion')
def ajouter(request):

    services = Service.objects.all()
    grades = Grade.objects.all()
    fonctions = Fonction.objects.all()
    echellons = Echellon.objects.all()
    statutgrades = Statutgrade.objects.all()
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()
    statuts = Statut.objects.all()

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
        adressear= request.POST["adressear"]
        adressefr = request.POST["adressefr"]
        numiden = request.POST["numiden"]
        daterec = request.POST["daterec"]
        datedec = request.POST["datedec"]
        dateretr = dateRetraiteCalc(daten)
        numcnopsaf = request.POST["numcnopsaf"]
        numcnopsim = request.POST["numcnopsim"]
        rib = request.POST["rib"]
        ancadmi = request.POST["ancadmi"]
        adminiapp = request.POST["adminiapp"]
        photo = request.FILES.get('photo')
        dategrade = request.POST["dategrade"]
        datestatut = request.POST["datestatut"]
        grade = request.POST["grade"]
        fonction = request.POST["fonction"]
        datefonction = request.POST["datefonction"]
        sexe = request.POST["sexe"]
        age = calculate_age(daten)
        ppr = request.POST["ppr"]
        statut = request.POST["statut"]
        echellon = request.POST["echellon"]
        dateechellon = request.POST["dateechellon"]
        indice = request.POST.get('indice', None)

        if (int(request.POST.get('situationfar', None)) == 1):
            situatar = "متزوج(ة)"
            situatfr = "marié(e)"
        elif (int(request.POST.get('situationfar', None)) == 2):
            situatar = "مطلق(ة)"
            situatfr = "divorcé(e)"
        else:
            situatar = "بدون"
            situatfr = "célibataire(e)"

        objperso = Personnel.objects.create(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr,
                            lieunaissancear=lieunar, lieunaissancefr=lieunfr, datenaissance=daten,
                            tele=tele, email=email, situationfamilialefr=situatfr, adressear=adressear,
                            adressefr=adressefr, numerofinancier=numiden, daterecrutement=daterec,
                            datedemarcation=datedec, dateparrainageretraite=dateretr, numcnopsaf=numcnopsaf,
                            numcnopsim=numcnopsim, rib=rib, ancienneteadmi=ancadmi, administrationapp=adminiapp,
                            situationfamilialear=situatar, photo=photo, sexe=sexe, age=age, lastupdate=datetime.date.today(),
                                           ppr=ppr)
        objperso.save()

        if (request.POST.get('entite', None) == "Secrétariat général"):
            service = request.POST["service"]
            dateservice = request.POST["dateservice"]
            objservice = Service(idservice=service)
            objserviceperso = Servicepersonnel.objects.create(idpersonnel_field=objperso, idservice_field=objservice,
                                                              dateaffectation=dateservice)
            objserviceperso.save()

            objperso.organisme = "Service"
            objperso.save()

        elif (request.POST.get('entite', None) == "Commandement"):
            if(request.POST.get('districtpashalik', None) == "District"):
                annexe = request.POST["annexe"]
                datesannexe= request.POST["dateannexe"]
                objannexe = Annexe(idannexe=annexe)
                objannexeperso = Annexepersonnel.objects.create(idpersonnel_field=objperso, idannexe_field=objannexe, dateaffectation=datesannexe)
                objannexeperso.save()

                objperso.organisme = "Annexe"
                objperso.save()

            elif(request.POST.get('districtpashalik', None) == "Pashalik"):
                pashalik = request.POST["pashalik"]
                datepashalik = request.POST["datepashalik"]
                objpashalik = Pashalik(idpashalik=pashalik)
                objpashalikperso = Pashalikpersonnel.objects.create(idpersonnel_field=objperso, idpashalik_field=objpashalik, dateaffectation=datepashalik)
                objpashalikperso.save()

                objperso.organisme = "Pashalik"
                objperso.save()

            elif((request.POST.get('districtpashalik', None) == "Cercle")):
                caidat = request.POST["caida"]
                datecaidat = request.POST["datecaida"]
                objcaidat = Caidat(idcaidat=caidat)
                objcaidatperso = Caidatpersonnel.objects.create(idpersonnel_field=objperso, idcaidat_field=objcaidat, dateaffectation=datecaidat)
                objcaidatperso.save()

                objperso.organisme = "Caida"
                objperso.save()

        objgrade = Grade(idgrade=grade)
        objfonction = Fonction(idfonction=fonction)
        objstatut = Statut(idstatut=statut)
        objechellon = Echellon.objects.get(echellon=echellon)

        objfonctionperso = Fonctionpersonnel.objects.create(idpersonnel_field=objperso, idfonction_field=objfonction, datefonction=datefonction)
        objstatutperso = Statutpersonnel.objects.create(idpersonnel_field=objperso, idstatut_field=objstatut, datestatut=datestatut)
        objgradeperso = Gradepersonnel.objects.create(idpersonnel_field=objperso, idgrade_field=objgrade, dategrade=dategrade,
                                                      idechellon_field=objechellon, dateechellon=dateechellon, indice=indice )



        objfonctionperso.save()
        objgradeperso.save()
        objstatutperso.save()

        conjoints = Conjointpersonnel.objects.filter(idpersonnel_field=objperso.idpersonnel).all()

        return render(request,'GestionPersonnel/ajouter.html', {'personnel': objperso})
    return render(request, 'GestionPersonnel/ajouter.html', {'services': services, 'grades': grades, 'fonctions': fonctions,
                                                             'echellons': echellons, 'statutgrades': statutgrades,
                                                             'entites': entites, 'pashaliks': pashaliks,
                                                             'districts': districts, 'divisions': divisions, 'cercles': cercles,
                                                             'statuts': statuts})


# modifier -------------------------------.
@login_required(login_url='/connexion')
def modifier(request, id):
    if request.method == 'POST':
        daten = request.POST["daten"]
        lieunar = request.POST["lieunar"]
        lieunfr = request.POST["lieunfr"]
        tele = request.POST["tele"]
        email = request.POST["email"]
        adressear = request.POST["adressear"]
        adressefr = request.POST["adressefr"]
        numiden = request.POST["numiden"]
        daterec = request.POST["daterec"]
        datedec = request.POST["datedec"]
        dateretr = request.POST["dateretr"]
        numcnopsaf = request.POST["numcnopsaf"]
        numcnopsim = request.POST["numcnopsim"]
        rib = request.POST["rib"]
        ancadmi = request.POST["ancadmi"]
        adminiapp = request.POST["adminiapp"]
        photo = request.POST["photo"]
        #service = request.POST["service"]
        #grade = request.POST["grade"]
        #fonction = request.POST["fonction"]
        sexe = request.POST["sexe"]
        age = calculate_age(daten)
        ppr = request.POST["ppr"]

        if (int(request.POST.get('situationfar', None)) == 1):
            situatar = "متزوج(ة)"
            situatfr = "marié(e)"
        elif (int(request.POST.get('situationfar', None)) == 2):
            situatar = "مطلق(ة)"
            situatfr = "divorcé(e)"
        else:
            situatar = "بدون"
            situatfr = "célibataire(e)"

        objperso2 = Personnel.objects.get(idpersonnel=id)
        objperso2.tele = tele
        objperso2.email = email
        objperso2.ppr = ppr
        objperso2.numcnopsaf = numcnopsaf
        objperso2.numcnopsim = numcnopsim
        objperso2.adressefr = adressefr
        objperso2.adressear = adressear
        objperso2.situationfamilialear = situatar
        objperso2.situationfamilialefr = situatfr
        objperso2.lieunaissancefr = lieunfr
        objperso2.lieunaissancear = lieunar
        objperso2.rib = int(rib)
        objperso2.datenaissance = daten
        objperso2.numerofinancier = numiden
        objperso2.datedemarcation = datedec
        objperso2.daterecrutement = daterec
        objperso2.dateparrainageretraite = dateretr
        objperso2.ancienneteadmi = ancadmi
        objperso2.administrationapp = adminiapp
        objperso2.photo = photo
        objperso2.sexe = sexe
        objperso2.age = age
        objperso2.lastupdate = datetime.date.today()
        objperso2.save()

        """objservice = Service(idservice=service)
        objgrade = Grade(idgrade=grade)
        objfonction = Fonction(idfonction=fonction)

        
        if not Fonctionpersonnel.objects.filter(idpersonnel_field=objperso2).filter(idfonction_field=objfonction):
            objfonctionperso = Fonctionpersonnel(idpersonnel_field=objperso2, idfonction_field=objfonction,
                                                 datefonction=datefonction)
            objfonctionperso.save()

        if not Servicepersonnel.objects.filter(idpersonnel_field=objperso2).filter(idservice_field=objservice):
            objserviceperso = Servicepersonnel(idpersonnel_field=objperso2, idservice_field=objservice,
                                           dateaffectation=dateservice)
            objserviceperso.save()

        if not Gradepersonnel.objects.filter(idpersonnel_field=objperso2).filter(idgrade_field=objgrade):
            objgradeperso = Gradepersonnel(idpersonnel_field=objperso2, idgrade_field=objgrade, dategrade=dategrade)
            objgradeperso.save()"""

    objperso = Personnel.objects.get(idpersonnel=id)

    conjointsinperso = Conjointpersonnel.objects.filter(idpersonnel_field=id)
    conjoints = Conjoint.objects.filter(idconjoint__in=conjointsinperso.values_list('idconjoint_field', flat=True))


    #   serviceperso = Servicepersonnel.objects.filter(idpersonnel_field=id).values_list('idservice_field', flat=True)
    #    servicelast = Service.objects.filter(idservice__in=serviceperso).last()
    #   servicepersolast = Servicepersonnel.objects.get(idpersonnel_field=objperso, idservice_field=servicelast)

    #    gradeperso = Gradepersonnel.objects.filter(idpersonnel_field=id).values_list('idgrade_field', flat=True)
    #    gradelast = Grade.objects.filter(idgrade__in=gradeperso).last()
    #    gradepersolast = Gradepersonnel.objects.get(idpersonnel_field=objperso, idgrade_field=gradelast)

    #    fonctionperso = Fonctionpersonnel.objects.filter(idpersonnel_field=id).values_list('idfonction_field', flat=True)
    #    fonctionlast = Fonction.objects.filter(idfonction__in=fonctionperso).last()
    #    fonctionpersolast = Fonctionpersonnel.objects.get(idpersonnel_field=objperso, idfonction_field=fonctionlast)

    #services = Service.objects.all()
    #grades = Grade.objects.all()
    #fonctions = Fonction.objects.all()

    enfants = Enfant.objects.filter(idconjoint_field__in=conjointsinperso.values_list('idconjoint_field', flat=True))
    diplomes = Diplome.objects.filter(idpersonnel_field=id)

    return render(request, 'GestionPersonnel/modifier.html',
                      {'personnel': objperso, 'conjoints': conjoints,
                       #'services': services,'grades': grades, 'fonctions':fonctions, 'servicelast': servicelast,
                       #'gradelast': gradelast,'fonctionlast': fonctionlast,
                       #'fonctionpersolast': fonctionpersolast,'servicepersolast':servicepersolast,'gradepersolast':gradepersolast,
                       'enfants': enfants, 'diplomes': diplomes})


# Reafectation -----------------------------------
@login_required(login_url='/connexion')
def addreaffectation(request):
    id = request.GET.get("id", None)
    date = request.GET.get("date", None)
    personnelFor = Personnel.objects.get(idpersonnel=id)
    objreaffectation = Reafectation.objects.filter(idpersonnel_field=personnelFor).first()

    if (objreaffectation.organisme == 'Service'):
        service = Service.objects.get(idservice=objreaffectation.idorganismeparent)
        objserviceperso = Servicepersonnel.objects.create(idpersonnel_field=personnelFor,idservice_field=service, dateaffectation=date)
        objserviceperso.save()
        personnelFor.organisme = 'Service'
        personnelFor.save()


    elif (objreaffectation.organisme == 'Pashalik'):
        pashalik = Pashalik.objects.get(idpashalik=objreaffectation.idorganismeparent)
        objpashalikperso = Pashalikpersonnel.objects.create(idpersonnel_field=personnelFor, idpashalik_field=pashalik,
                                                          dateaffectation=date)
        objpashalikperso.save()
        personnelFor.organisme = 'Pashalik'
        personnelFor.save()


    elif (objreaffectation.organisme == 'Cercle'):
        caidat = Caidat.objects.get(idcaidat=objreaffectation.idorganismeparent)
        objscaidatperso = Caidatpersonnel.objects.create(idpersonnel_field=personnelFor, idcaidat_field=caidat,
                                                           dateaffectation=date)
        objscaidatperso.save()
        personnelFor.organisme = 'Caidat'
        personnelFor.save()


    elif(objreaffectation.organisme == 'Annexe'):
        annexe = Annexe.objects.get(idannexe=objreaffectation.idorganismeparent)
        objsannexeperso = Annexepersonnel.objects.create(idpersonnel_field=personnelFor, idannexe_field=annexe,
                                                         dateaffectation=date)
        objsannexeperso.save()
        personnelFor.organisme = 'Annexe'
        personnelFor.save()

    Reafectation.objects.filter(idreafectation=objreaffectation.idreafectation).delete()
    return redirect('/personnel/reaffectation')


@login_required(login_url='/connexion')
def deletereaffectation(request, id):
    Reafectation.objects.filter(idreafectation=id).delete()
    return redirect('/personnel/reaffectation')

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxloadadministration(request):
    objpersonneladmi = {'personnels': list(Personnel.objects.filter(administrationapp=request.POST.get("administration", None)).values('idpersonnel','nomar','nomfr','cin','prenomar','prenomfr'))}
    return JsonResponse(objpersonneladmi, safe=False)

@login_required(login_url='/connexion')
@csrf_exempt
def ajaxloadpersonnel(request):
    personnelFor = Personnel.objects.filter(idpersonnel=request.POST['personnel']).first()
    personnel = Personnel.objects.filter(idpersonnel=request.POST['personnel'])
    objgradeperso = Gradepersonnel.objects.filter(idpersonnel_field=personnelFor)
    objreaffectation = Reafectation.objects.filter(idpersonnel_field=personnelFor)


    if(personnelFor.organisme == 'Service'):
        objserviceperso = Servicepersonnel.objects.filter(idpersonnel_field=personnelFor)
        data = {'persodata': {'idpersonnel': personnel.values_list('idpersonnel').first(),
                              'nomar': personnel.values_list('nomar').first(),
                              'prenomar': personnel.values_list('prenomar').first(),
                              'ppr': personnel.values_list('ppr').first(),
                              'oraganisme': objserviceperso.values_list('idservice_field__libelleservicear').last(),
                              'grade': objgradeperso.values_list('idgrade_field__gradear').last(),
                              'reafectation': objreaffectation.values_list('idreafectation','libellereafectationar').first()}}

        return JsonResponse(data, safe=False)
    elif(personnelFor.organisme == 'Pashalik'):
        objpashalikperso = Pashalikpersonnel.objects.filter(idpersonnel_field=personnelFor)
        data = {'persodata': {'idpersonnel': personnel.values_list('idpersonnel').first(),
                              'nomar': personnel.values_list('nomar').first(),
                              'prenomar': personnel.values_list('prenomar').first(),
                              'ppr': personnel.values_list('ppr').first(),
                              'oraganisme': objpashalikperso.values_list('idpashalik_field__libellepashalikar').last(),
                              'grade': objgradeperso.values_list('idgrade_field__gradear').last(),
                              'reafectation': objreaffectation.values_list('idreafectation','libellereafectationar').first()}}
        return JsonResponse(data, safe=False)

    elif(personnelFor.organisme == 'Cercle'):
        objcaidatperso = Caidatpersonnel.objects.filter(idpersonnel_field=personnelFor)
        data = {'persodata': {'idpersonnel': personnel.values_list('idpersonnel').first(),
                              'nomar': personnel.values_list('nomar').first(),
                              'prenomar': personnel.values_list('prenomar').first(),
                              'ppr': personnel.values_list('ppr').first(),
                              'oraganisme': objcaidatperso.values_list('idcaidat_field__libellecaidatar').last(),
                              'grade': objgradeperso.values_list('idgrade_field__gradear').last(),
                              'reafectation': objreaffectation.values_list('idreafectation','libellereafectationar').first()}}
        return JsonResponse(data, safe=False)

    else:
        objannexeperso = Annexepersonnel.objects.filter(idpersonnel_field=personnelFor )
        data = {'persodata': {'idpersonnel': personnel.values_list('idpersonnel').first(),
                              'nomar': personnel.values_list('nomar').first(),
                              'prenomar': personnel.values_list('prenomar').first(),
                              'ppr': personnel.values_list('ppr').first(),
                              'oraganisme': objannexeperso.values_list('idannexe_field__libelleannexear').last(),
                              'grade': objgradeperso.values_list('idgrade_field__gradear').last(),
                              'reafectation': objreaffectation.values_list('idreafectation','libellereafectationar').first()}}
        return JsonResponse(data, safe=False)

@login_required(login_url='/connexion')
def reaffectation(request):
    grades = Grade.objects.all()
    fonctions = Fonction.objects.all()
    echellons = Echellon.objects.all()
    statutgrades = Statutgrade.objects.all()
    entites = Entite.objects.all()
    pashaliks = Pashalik.objects.all()
    districts = District.objects.all()
    divisions = Division.objects.all()
    cercles = Cercle.objects.all()
    personnels = Personnel.objects.all()

    if request.method == 'POST':
        objperso = Personnel.objects.get(idpersonnel = request.POST.get("personnel"))

        if (request.POST.get('entite', None) == "Commandement"):
            if(request.POST.get('districtpashalik', None) == "District"):
                objannexe = Annexe.objects.get(idannexe=request.POST['annexe'])
                objReaffectationanne = Reafectation.objects.create(idpersonnel_field=objperso,
                                                                   libellereafectationar=objannexe.libelleannexear,
                                                                   libellereafectationfr=objannexe.libelleannexefr,
                                                                   idorganismeparent=objannexe.idannexe,
                                                                   organisme='Annexe')
                objReaffectationanne.save()


            elif(request.POST.get('districtpashalik', None) == "Pashalik"):
                pashalik = request.POST.get('pashalik', None)
                objpashalik = Pashalik.objects.get(idpashalik=pashalik)
                objReafectationpash = Reafectation.objects.create(idpersonnel_field=objperso,
                                                                  libellereafectationfr=objpashalik.libellepashalikfr
                                                                  ,libellereafectationar=objpashalik.libellepashalikar,
                                                                  idorganismeparent=objpashalik.idpashalik, organisme='Pashalik')
                objReafectationpash.save()

            elif((request.POST.get('districtpashalik', None) == "Cercle")):
                caidat = request.POST.get('caida', None)
                objcaidat = Caidat(idcaidat=caidat)
                objReafectationcaidat = Reafectation.objects.create(idpersonnel_field=objperso,
                                                                    libellereafectationar=objcaidat.libellecaidatar
                                                                    , libellereafectationfr=objcaidat.libellecaidatfr
                                                                    , idorganismeparent=objcaidat.idcaidat,
                                                                    organisme='Caidat')
                objReafectationcaidat.save()
        else:

            objservice = Service.objects.get(idservice=request.POST.get('service'))
            objReaffectationserv = Reafectation.objects.create(idpersonnel_field=objperso,
                                                               libellereafectationfr=objservice.libelleservicefr,
                                                               libellereafectationar=objservice.libelleservicear,
                                                               idorganismeparent=objservice.idservice, organisme='Service')
            objReaffectationserv.save()

    return render(request, 'GestionPersonnel/reaffectation.html', {'grades': grades, 'fonctions': fonctions,
                                                                   'echellons': echellons, 'statutgrades': statutgrades,
                                                                   'entites': entites, 'pashaliks': pashaliks,
                                                                   'districts': districts, 'divisions': divisions,
                                                                   'cercles': cercles, 'personnels': personnels})

# conjoint -----------------------------------
@login_required(login_url='/connexion')
def ajouter_conjoint(request):
    if request.method == 'POST':
        nomfr = request.POST["nomfr"]
        nomar = request.POST["nomar"]
        prenomfr = request.POST["prenomfr"]
        prenomar = request.POST["prenomar"]
        cin = request.POST["cin"]
        daten = request.POST["daten"]
        lieun = request.POST["lieun"]
        fonction = request.POST["fonction"]
        ppr = request.POST.get("ppr", None)

        personnelcin = request.POST["personnelcin"]
        obj1 = Conjoint(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr, lieunaissance=lieun, datenaissance=daten, ppr=ppr, fonction=fonction)
        obj1.save()
        pers = Personnel.objects.filter(cin=personnelcin).first()
        con = Conjoint.objects.filter(cin=cin).first()
        obj2 = Conjointpersonnel(idconjoint_field=con, idpersonnel_field=pers)
        obj2.save()
    else:
        cinpersonnel = request.GET.get('personnel', None)
        if(cinpersonnel) :
            return render(request, 'GestionPersonnel/ajouter_conjoint.html', {'personnel': cinpersonnel})
        else:
            return render(request, 'GestionPersonnel/ajouter_conjoint.html')
    if(obj1)  :
        return render(request, 'GestionPersonnel/ajouter_conjoint.html', {'conjoint' : obj1 ,'personnel': pers.cin})
    else:
        return render(request, 'GestionPersonnel/ajouter_conjoint.html')


@login_required(login_url='/connexion')
def modifier_conjoint(request,id):
    suc = "no"
    conjoint = Conjoint.objects.get(idconjoint=id)
    if request.method == 'POST':
        objconjoint = Conjoint.objects.get(idconjoint=id)
        objconjoint.nomfr = request.POST["nomfr"]
        objconjoint.nomar = request.POST["nomar"]
        objconjoint.prenomfr = request.POST["prenomfr"]
        objconjoint.prenomar = request.POST["prenomar"]
        objconjoint.cin = request.POST["cin"]
        objconjoint.datenaissance = request.POST["daten"]
        objconjoint.lieunaissance = request.POST["lieun"]
        objconjoint.ppr = request.POST.get("ppr", None)
        objconjoint.fonction = request.POST["fonction"]

        suc = "yes"
        objconjoint.save()
    return render(request, "GestionPersonnel/modifier_conjoint.html", {'conjoint': conjoint,'suc':suc})


# enfant -----------------------------------
@login_required(login_url='/connexion')
def ajouter_enfant(request):
    cinpersonnel = request.GET.get('personnel', None)
    personnel = Personnel.objects.filter(cin=cinpersonnel).first()
    conjointsinperso = Conjointpersonnel.objects.filter(idpersonnel_field=personnel)
    conjoints = Conjoint.objects.filter(idconjoint__in=conjointsinperso.values_list('idconjoint_field', flat=True))

    if request.method == 'POST':
        nomfr = request.POST["nomfr"]
        nomar = request.POST["nomar"]
        prenomfr = request.POST["prenomfr"]
        prenomar = request.POST["prenomar"]
        lienj = request.POST["lienj"]
        daten = request.POST["daten"]
        lieunfr = request.POST["lieunfr"]
        lieunar = request.POST["lieunar"]
        mere = request.POST["mere"]
        objenfant = Enfant(nomar=nomar, nomfr=nomfr, lienjuridique=lienj, prenomar=prenomar, prenomfr=prenomfr,
                           lieunaissancefr=lieunfr, lieunaissancear=lieunar, datenaissance=daten, idconjoint_field= Conjoint.objects.get(idconjoint=mere))
        objenfant.save()
        return render(request, 'GestionPersonnel/ajouter_enfant.html', {'enfant': Enfant.objects.all(),'personnel': cinpersonnel, 'conjoints':conjoints})
    return render(request, 'GestionPersonnel/ajouter_enfant.html', {'personnel': cinpersonnel, 'conjoints':conjoints})

@login_required(login_url='/connexion')
def modifier_enfant(request,id):
    suc = 'no'
    objenfant = Enfant.objects.get(idenfant=id)
    conjoints = Conjoint.objects.all()
    if request.method == "POST":
        objenfant.nomfr = request.POST["nomfr"]
        objenfant.nomar = request.POST["nomar"]
        objenfant.prenomfr = request.POST["prenomfr"]
        objenfant.prenomar = request.POST["prenomar"]
        objenfant.lienjuridique = request.POST["lienj"]
        objenfant.datenaissance = request.POST["daten"]
        objenfant.lieunaissancefr = request.POST["lieunfr"]
        objenfant.lieunaissancear = request.POST["lieunar"]
        objenfant.idconjoint_field = Conjoint.objects.get(idconjoint=request.POST["mere"])
        objenfant.save()
        suc = 'yes'
    return render(request, 'GestionPersonnel/modifier_enfant.html', {'enfant': objenfant, 'conjoints':conjoints,'suc':suc})

# diplome -----------------------------------
@login_required(login_url='/connexion')
def ajouter_diplome(request):
    cinpersonnel = request.GET.get('personnel', None)
    personnel = Personnel.objects.filter(cin=cinpersonnel).first()
    if request.method == 'POST':
        diplomefr = request.POST["diplomefr"]
        diplomear = request.POST["diplomear"]
        etabfr = request.POST["etabfr"]
        etabar = request.POST["etabar"]
        spefr = request.POST["spefr"]
        spear= request.POST["spear"]
        datedip = request.POST["datedip"]
        objdiplome=Diplome(diplomefr=diplomefr, diplomear=diplomear, etablissement=etabfr,
                           specialitear=spear, specialitefr=spefr, datediplome=datedip,idpersonnel_field=personnel)
        objdiplome.save()
        return render(request, 'GestionPersonnel/ajouter_diplome.html', {'personnel': cinpersonnel, 'diplome':objdiplome})
    return render(request, 'GestionPersonnel/ajouter_diplome.html', {'personnel': cinpersonnel})


@login_required(login_url='/connexion')
def modifer_diplome(request,id):
    suc = 'no'
    objdiplome = Diplome.objects.get(iddiplome=id)
    if request.method == 'POST':
        objdiplome.diplomefr = request.POST["diplomefr"]
        objdiplome.diplomear = request.POST["diplomear"]
        objdiplome.etablissement = request.POST["etabfr"]
        objdiplome.specialitefr = request.POST["spefr"]
        objdiplome.specialitear = request.POST["spear"]
        objdiplome.datediplome = request.POST["datedip"]
        objdiplome.save()
        suc = 'yes'
    return render(request, 'GestionPersonnel/modifier_diplome.html',
                  {'diplome': objdiplome, 'suc': suc})

# Attestations ---------------------------
@login_required(login_url='/connexion')
def printpdfquitter(req,id):
    personnel = Personnel.objects.get(idpersonnel=id)
    gradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=personnel).last()
    quitterterritoirelast = QuitterTerritoire.objects.all().last()
    if (quitterterritoirelast == None):
        dataattes = 1
    else:
        dataattes = quitterterritoirelast.numquitterterritoire + 1;
    if (gradepersonnel == None):
        datagrade = " "
    else:
        datagrade = gradepersonnel.idgrade_field.gradefr
    attestation = QuitterTerritoire()
    attestation.numquitterterritoire = dataattes;
    attestation.idpersonnel_field = personnel
    attestation.datedelivre = datetime.date.today()
    attestation.save()
    empName = str(personnel.nomfr + " " + personnel.prenomfr)
    cin = str(personnel.cin)
    grade=datagrade;
    temp=req.POST["De"]
    du=req.POST["Da"]
    anne=req.POST["an"]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=9)
    pdf.text(23, 15, txt="ROYAUME DU MAROC ")
    pdf.text(19, 21, txt="MINISTERE DE L'INTERIEUR ")
    pdf.text(15, 27, txt="WILAYA DE LA REGION L'ORIENTAL ")
    pdf.text(16, 33, txt="PREFECTURE D'OUJDA ANGAD ")
    pdf.text(23, 39, txt="SECRETARIAT GENERAL ")
    pdf.text(12, 45, txt="DIVISION DU RESSOURCES HUMAINES  ")
    pdf.text(14, 51, txt="ET DES AFFAIRES ADMINISTRATIVES ")
    pdf.text(14, 57, txt="N°:  " + str(dataattes))
    pdf.image(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/images/logorm.png"), x=95, y=20, w=27)
    ##pdf.cell(100,100,"Attestation de travail",1,2,"c")
    pdf.set_font("Arial", "B", size=15)
    pdf.text(71, 78, txt="AUTORISATION DE QUITTER")
    pdf.text(74, 85, txt="LE TERRITOIRE NATIONAL")
    pdf.rect(66, 69, 87, 20)
    pdf.set_font("Arial", "B", size=12)
    pdf.text(30, 105, txt="Le Wali de la Région de l'Oriental,Gouverneur de Préfecture d'Oujda-Angad ")
    pdf.set_font("Arial", size=12)
    pdf.text(27, 112, txt="- Vu le Dahir N1.58.008 du 4 Chaàbane 1337 (24 février 1958) portant statut général ")
    pdf.text(23, 119, txt="de la fonction publique")
    pdf.text(27, 127, txt="- Vu le Dahir N1.11.10 du 14 Rabii 1er 1432 (18 février 2011) portant promulgation de ")
    pdf.text(23, 135,txt="la loi n 50-05 modifiant et complétant le dahir n1-58-008 du 4 chaàbane 1377 (24 février 1958)")
    pdf.text(23, 142, txt="portant statut général de la fonction publique")
    pdf.text(29, 149, txt="- Vu la demande présentée par l'intéressé(e). ")
    pdf.set_font("Arial", size=12)
    pdf.text(23, 160, txt="Autorise Mr(Mme)       :")
    pdf.text(23, 169, txt="Grade                          :")
    pdf.text(23, 178, txt="Titulaire de la C.N.I     :")
    pdf.set_font("Arial", "B", size=12)
    pdf.text(75, 160, txt=empName)
    pdf.text(75, 169, txt=grade)
    pdf.text(75, 178, txt=cin)
    pdf.set_font("Arial", size=12)
    pdf.text(102, 178, txt="à bénéficier de son congé au titre de l'année "+anne)
    pdf.text(23, 190, txt="De                               :")
    pdf.text(125, 190, txt="à l'étranger:")
    pdf.text(23, 199, txt="Et ce compter du        :")
    pdf.set_font("Arial", "B", size=12)
    pdf.text(75, 190, txt=temp+" jours  ouvrables  ")
    pdf.text(75, 199, txt=du)
    pdf.set_font("Arial", size=12)
    pdf.text(32, 209, txt="En foi de quoi la présente autorisation est délivrée à l'intéressé(e) pour sévir  ")
    pdf.text(23, 217, txt="et valoir ce que de droit ")

    pdf.text(125, 250, txt="Oujda le :")
    ##pdf.cell(80)
    ##pdf.cell(60,10,'Attestation de Travaille',1,1,'C');
    pdf.output("test.pdf")
    pdfr = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdfr, content_type='application/pdf')
    response['Content-Disposition'] = 'filename='+ empName+str(dataattes)+'.pdf';
    ##response.TransmitFile(pathtofile);
    return (response)


@login_required(login_url='/connexion')
def printpdf(req,id):
   personnel = Personnel.objects.get(idpersonnel=id)
   empName = str(personnel.nomfr + " " + personnel.prenomfr)
   gradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=personnel).last()
   attestationlast = Attestationtravail.objects.all().last()
   if(attestationlast == None):
       dataattes = 1
   else:
       dataattes = attestationlast.numattestationtravail + 1;
   if(gradepersonnel == None):
       datagrade = " "
   else:
       datagrade = gradepersonnel.idgrade_field.gradefr
   attestation = Attestationtravail()
   attestation.numattestationtravail=dataattes;
   attestation.idpersonnel_field=personnel
   attestation.datedelivre=datetime.date.today()
   attestation.save()
   pdf=FPDF()
   pdf.add_page()
   pdf.set_font("Arial",size=9)
   pdf.text(23,15,txt="ROYAUME DU MAROC ")
   pdf.text(19,21,txt="MINISTERE DE L'INTERIEUR ")
   pdf.text(15,27,txt="WILAYA DE LA REGION L'ORIENTAL ")
   pdf.text(16,33,txt="PREFECTURE D'OUJDA ANGAD ")
   pdf.text(23,39,txt="SECRETARIAT GENERAL ")
   pdf.text(12,45,txt="DIVISION DU RESSOURCES HUMAINES  ")
   pdf.text(14,51,txt="ET DES AFFAIRES ADMINISTRATIVES ")
   pdf.text(14, 57, txt="N°:  "+str(dataattes))
   pdf.image(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/images/logorm.png"), x=95     , y=20, w=27)
   ##pdf.cell(100,100,"Attestation de travail",1,2,"c")
   pdf.set_font("Arial", size=15)
   pdf.text(80,87,txt="Attestation de travail")
   pdf.rect(70,80,70,10)
   pdf.rect(12, 105, 190, 140)
   pdf.set_font("Arial", "B",size=12)
   pdf.text(36,116,txt="Le Wali de la Région de l'Oriental,Gouverneur de Préfecture d'Oujda-Angad ")
   pdf.set_font("Arial", size=11)
   pdf.text(25,130,txt="Atteste que Me/Mme    :          "+empName)
   pdf.text(25,138,txt="Titulaire de la C.N.I      :          "+str(personnel.cin))
   pdf.text(25,146,txt="P.P.R                           :          "+str(personnel.numerofinancier))
   pdf.text(25,160,txt="Exerce à la Wilaya de la Région de l'Oriental,Préfecture d'Oujda-Angad")
   pdf.text(25,170,txt="En qualité de                :         "+str(datagrade))
   pdf.text(25,185,txt="En foi de quoi,la présente attestation est délivrée à l'intéressé(e) pour servir et voir ce que de droit ")
   pdf.text(125, 200, txt="Oujda le :         "+str(datetime.date.today()))
   ##pdf.cell(80)
   ##pdf.cell(60,10,'Attestation de Travaille',1,1,'C');
   pdf.output("test.pdf")
   pdfr = pdf.output(dest='S').encode('latin-1')
   response = HttpResponse(pdfr,content_type='application/pdf')
   name=empName+str(dataattes)
   response['Content-Disposition'] = 'filename='+name+'.pdf'
   ##response.TransmitFile(pathtofile);
   return (response)
   #return FileResponse(open('foobar.pdf', 'rb'), content_type='application/pdf')


def printpdfar(req, id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    personnel = Personnel.objects.get(idpersonnel=id)
    empName = str(personnel.nomfr + " " + personnel.prenomfr)
    gradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=personnel).last()
    attestationlast = Attestationtravail.objects.all().last()
    if (attestationlast == None):
        dataattes = 1
    else:
        dataattes = attestationlast.numattestationtravail + 1;
    if (gradepersonnel == None):
        grade = " "
    else:
        grade = gradepersonnel.idgrade_field.gradefr

    attestation = Attestationtravail()
    attestation.numattestationtravail = dataattes;
    attestation.idpersonnel_field = personnel
    attestation.datedelivre = datetime.date.today()
    attestation.save()

    fontdir = os.path.join(BASE_DIR, 'static/filefonts/')
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', os.path.join(fontdir, 'DejaVuSansMono.ttf'), uni=True)
    pdf.set_font("DejaVu", size=11)
    pdf.text(28+137, 10, txt=get_display(arabic_reshaper.reshape('المملكة المغربية')))
    pdf.text(30+137, 16, txt=get_display(arabic_reshaper.reshape("وزارة الداخلية")))
    pdf.text(28+137, 22, txt=get_display(arabic_reshaper.reshape('ولاية جهة الشرق')))
    pdf.text(28+137, 28, txt=get_display((arabic_reshaper.reshape('عمالة وجدة أنكاد'))))
    pdf.text(31+137, 34, txt=get_display(arabic_reshaper.reshape('الكتابة العامة')))
    pdf.text(25+137, 40, txt=get_display(arabic_reshaper.reshape('قسم الموارد البشرية')))
    pdf.text(28+137, 46, txt=get_display(arabic_reshaper.reshape('والشؤون الإدارية')))
    pdf.text(40+137, 55,txt=get_display(arabic_reshaper.reshape('رقم : '+ str(dataattes) )))

    #pdf.text(14, 51, txt="ET DES AFFAIRES ADMINISTRATIVES ")
    pdf.image(os.path.join(BASE_DIR, "static/images/Picture1.png"), x=92, y=20, w=27)
    ##pdf.cell(100,100,"Attestation de travail",1,2,"c")
    pdf.add_font('DejaVuSMB', '', os.path.join(fontdir, 'DejaVuSansMono-Bold.ttf'), uni=True)
    pdf.set_font("DejaVuSMB", size=18)
    #pdf.set_font('Arial','B',size=15)
    pdf.text(90, 71, txt=get_display(arabic_reshaper.reshape('شهادة عمل')))
    pdf.rect(63, 60, 87, 20)
    pdf.add_font('DejaVuSC', '', os.path.join(fontdir, 'DejaVuSansCondensed.ttf'), uni=True)
    pdf.set_font('DejaVuSC', size=14)
    pdf.text(55, 107, txt=get_display(arabic_reshaper.reshape('يشـهـد والي جهـة الشـرق، عـامل عـمالـة وجـدة أنكَاد')))
    pdf.set_font('DejaVuSC', size=13)
    pdf.text(168, 134, txt=get_display(arabic_reshaper.reshape('أن السيد(ة):')))
    pdf.text(97-len(personnel.nomar+' '+personnel.prenomar), 134, txt=get_display(arabic_reshaper.reshape(personnel.nomar+' '+personnel.prenomar)))
    pdf.text(119, 148, txt=get_display(arabic_reshaper.reshape('الحامل(ة) للبطاقة الوطنية للتعريف رقم :')))
    pdf.text(97-len(personnel.cin), 148, txt=str(personnel.cin))
    pdf.text(160, 162, txt=get_display(arabic_reshaper.reshape('رقـــم التــــأجير ')))
    pdf.text(119, 162, txt=':')
    pdf.text(97 - len(personnel.ppr), 162, txt=str(personnel.ppr))
    pdf.text(68, 176, txt=get_display(arabic_reshaper.reshape('موظف(ة) بولاية جهة الشرق عمالة وجدة أنكَاد')))
    pdf.text(173, 190, txt=get_display(arabic_reshaper.reshape('بدرجـــة: ')))
    pdf.text(97-len(grade), 190, txt=get_display(arabic_reshaper.reshape(grade)))
    pdf.text(56, 204, txt=get_display((arabic_reshaper.reshape('وسلمت هذه الشـهادة للمعني(ة) بالأمر بطلب منه(ها) للإدلاء بهـا عـند الحـاجـة.'))))
    pdf.text(52, 224, txt=get_display(arabic_reshaper.reshape('وجــدة في:')))
    pdf.rect(15, 95, 180, 175)
    ##pdf.cell(80)
    ##pdf.cell(60,10,'Attestation de Travaille',1,1,'C');
    pdf.output("test.pdf")
    pdfr = pdf.output(dest='S').encode('latin-1')
    response = HttpResponse(pdfr, content_type='application/pdf')
    response['Content-Disposition'] = 'filename='+ empName+str(dataattes)+'.pdf';
    ##response.TransmitFile(pathtofile);
    return response
@login_required(login_url='/connexion')
@csrf_exempt
def ajaxtaboardpersonnel(request):

    date = request.POST.get('annes', None)
    if date == None:
        date = datetime.datetime.now().year
    else:
        date = int(date)

    # date1
    departretraite = []
    departretraiteonecount = []
    departretraitetwocount = []
    i = 0
    while i <= 11:
        departretraiteonecount.append(Personnel.objects.filter(administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral').filter(dateparrainageretraite__year=date).filter(dateparrainageretraite__month=i + 1).count())
        departretraitetwocount.append(Personnel.objects.filter(administrationapp='عمالة وجدة أنجاد-Général').filter(dateparrainageretraite__year=date).filter(dateparrainageretraite__month=i + 1).count())
        i = i + 1

    departretraite = {
                      'departretraite' : list(Personnel.objects.filter(dateparrainageretraite__year=date).values('cin','nomar','nomfr','age','idpersonnel')),
                      'departretraitetwocount' : departretraitetwocount,
                      'departretraiteonecount': departretraiteonecount}

    return JsonResponse(departretraite,safe=False)


#taboard------------------------------------------------------
@login_required(login_url='/connexion')
@csrf_exempt
def taboardpersonnel(request):

    femmes = Personnel.objects.filter(sexe='Femme-أنثى').count()
    hommes = Personnel.objects.filter(sexe='Homme-ذكر').count()
    personnels = Personnel.objects.all().count()
    data = datetime.datetime.today() - datetime.timedelta(days=6 * 365/12)
    personnelslastup = Personnel.objects.filter(lastupdate__lte = data).all()
    administrationOne = Personnel.objects.filter(administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral').count()
    administrationTwo = Personnel.objects.filter(administrationapp='عمالة وجدة أنجاد-Général').count()

    # dates 5 retraites
    i = 0
    cinqdepartretraite = []
    while i < 5:
        data = {'cinqdepartretraite' : Personnel.objects.filter(dateparrainageretraite__year=datetime.datetime.now().year + i).count(),
                'an' : datetime.datetime.now().year + i,
                'cinqdepartretraiteone': Personnel.objects.filter(administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral').filter(dateparrainageretraite__year=datetime.datetime.now().year + i).count(),
                'cinqdepartretraitetwo' : Personnel.objects.filter(administrationapp='عمالة وجدة أنجاد-Général').filter(dateparrainageretraite__year=datetime.datetime.now().year + i).count()
                }
        cinqdepartretraite.append(data)
        i = i + 1

    #date1
    departretraiteone = []
    i = 0
    while i <= 11:
        departretraiteone.append(Personnel.objects.filter(administrationapp='مجلس عمالة وجدة أنجاد-Préfectoral').filter(
            dateparrainageretraite__year=datetime.datetime.now().year).filter(dateparrainageretraite__month=i+1).count())
        i = i + 1

    #date2
    departretraitetwo = []
    i = 0
    while i<=11:
        departretraitetwo.append(Personnel.objects.filter(administrationapp='عمالة وجدة أنجاد-Général').filter(
            dateparrainageretraite__year=datetime.datetime.now().year).filter(dateparrainageretraite__month=i+1).count())
        i = i + 1

    """[-13932000, -11020000, -7611000, -4653000, -1952000, -625000, -116000, -14000, -1000]
    [14220000, 10125000, 5984000, 3131000, 1151000, 312000, 49000, 4000, 0]"""

    ageData = pd.DataFrame(
        {
            'Age': ['20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],
            'Male': count_age_int('Homme-ذكر'),
            'Female': [-x for x in count_age_int('Femme-أنثى')],
        }
    )
    AgeClass = [ '60-64', '55-59', '50-54', '45-49', '40-44', '35-39', '30-34', '25-29', '20-24']
    pallette = sns.color_palette("Blues")
    bar_plot = sns.barplot(x='Male', y='Age', data=ageData, order=AgeClass, lw=0, palette = pallette).set_title('ﺭﺎﻤﻋﻷﺍ ﻡﺮﻫ')
    bar_plot = sns.barplot(x='Female', y='Age', data=ageData, order=AgeClass, lw=0, palette = pallette)
    bar_plot.set_xlabel("Population")
    chart = get_graph()


    return render(request,'GestionPersonnel/tboardpersonnel.html',
        {
            'femmes': femmes,
            'hommes': hommes,
            'personnels': personnels,
            'administrationOne': administrationOne,
            'administrationTwo': administrationTwo,
            'departretraiteone': departretraiteone,
            'departretraitetwo': departretraitetwo,
            'chart': chart,
            'personnelslastup': personnelslastup,
            'cinqdepartretraite' : cinqdepartretraite,
        })


