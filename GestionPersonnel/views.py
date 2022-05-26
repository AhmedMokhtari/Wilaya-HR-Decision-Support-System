from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
from django.http import HttpResponse, JsonResponse
import os
import datetime
import csv
import pandas as pd
import seaborn as sns
from .utils import calculate_age, get_graph, count_age_int, dictfetchall
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.db import connection


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
    division = Division.objects.all();
    grade = Grade.objects.all();
    personnels = {'personnels': rows, 'divs': division, 'grades': grade}
    return render(request, 'GestionPersonnel/consultation.html', personnels)
#perso info img
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
    reqAncienteAdmi = "P.{ancienneteAdmi} = '{ancienneteAdmiValue}' ".format(ancienneteAdmi=arr[0], ancienneteAdmiValue=arr[1]);
    reqDivision = " D.{IdDivision}='{IdDivisionValue}'".format( IdDivision=arr[2], IdDivisionValue=arr[3]);
    reqGrade = " G.{IdGrade}='{IdGradeValue}'".format( IdGrade=arr[4], IdGradeValue=arr[5]);
    reqgenre = " P.{Sexe}='{SexeValue}'".format( Sexe=arr[6], SexeValue=arr[7]);
    if(arr[0]==str(1) and arr[1]==str(1)):
        reqAncienteAdmi="1 = 1"
    if (arr[2] == str(1) and arr[3] == str(1)):
        reqDivision = "1 = 1"
    if (arr[4] == str(1) and arr[5] == str(1)):
        reqGrade = "1 = 1"
    if (arr[6] == str(1) and arr[7] == str(1)):
        reqgenre = "1 = 1"
    cursor = connection.cursor()
    req='''with t1 as(select IdService#,IdPersonnel#,DateAffectation, ROW_NUMBER()  OVER ( PARTITION BY IdPersonnel# ORDER BY IdPersonnel#,DateAffectation desc ) RowNumber from ServicePersonnel )
    ,
    t2 as(
    select IdGrade#,IdPersonnel#,DateGrade, ROW_NUMBER()  OVER ( PARTITION BY IdPersonnel# ORDER BY IdPersonnel#,DateGrade desc ) RowNumber from GradePersonnel
    )
    select P.IdPersonnel,P.Sexe,P.Ppr, P.NomFr , P.PrenomFr,P.Cin,P.photo,D.LibelleDivisionFr, S.LibelleServiceFr ,P.AdministrationApp ,t1.IdService#,t1.DateAffectation,t2.IdGrade#,t2.DateGrade,G.GradeFr,S.LibelleServiceFr
    from t1,t2 ,Service S ,Personnel P,Division D,Grade G where   t1.IdPersonnel# = t2.IdPersonnel#  and  t1.RowNumber = t2.RowNumber  and
    t1.RowNumber=1 AND S.IdService=t1.IdService# AND P.IdPersonnel=t1.IdPersonnel# AND D.IdDivision=S.IdDivision# AND G.IdGrade=t2.IdGrade# AND {reqAncienteAdmi} AND {reqDivision} AND {reqGrade}  AND {reqGenre} '''.format(reqAncienteAdmi=reqAncienteAdmi,reqDivision=reqDivision,reqGrade=reqGrade,reqGenre=reqgenre)
    cursor.execute(req)
    print(req);
    rows = list(dictfetchall(cursor))
    objpersonnel = list(Personnel.objects.filter(ancienneteadmi=selected_obj).values())
    return JsonResponse({'data':rows})

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


# ajouter -------------------------------.
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
    elif(statutgrade.statutgradefr == "Ingénieur et Architectes"):
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
        dateretr = request.POST["dateretr"]
        numcnopsaf = request.POST["numcnopsaf"]
        numcnopsim = request.POST["numcnopsim"]
        rib = request.POST["rib"]
        ancadmi = request.POST["ancadmi"]
        adminiapp = request.POST["adminiapp"]
        photo = request.FILES.get('photo')
        dategrade = request.POST["dategrade"]
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

        objperso= Personnel.objects.create(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr,
                            lieunaissancear=lieunar, lieunaissancefr=lieunfr, datenaissance=daten,
                            tele=tele, email=email, situationfamilialefr=situatfr, adressear=adressear,
                            adressefr=adressefr, numerofinancier=numiden, daterecrutement=daterec,
                            datedemarcation=datedec, dateparrainageretraite=dateretr, numcnopsaf=numcnopsaf,
                            numcnopsim=numcnopsim, rib=rib, ancienneteadmi=ancadmi, administrationapp=adminiapp,
                            situationfamilialear=situatar, photo=photo, sexe=sexe, age=age, lastupdate=datetime.date.today(),
                                           ppr=ppr, statut=statut)
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

                objperso.organisme = "pashalik"
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
        objechellon = Echellon.objects.get(echellon=echellon)

        objfonctionperso = Fonctionpersonnel.objects.create(idpersonnel_field=objperso, idfonction_field=objfonction, datefonction=datefonction)

        objgradeperso = Gradepersonnel.objects.create(idpersonnel_field=objperso, idgrade_field=objgrade, dategrade=dategrade,
                                                      idechellon_field=objechellon, dateechellon=dateechellon, indice=indice )



        objfonctionperso.save()
        objgradeperso.save()

        conjoints = Conjointpersonnel.objects.filter(idpersonnel_field=objperso.idpersonnel).all()

        return render(request,'GestionPersonnel/ajouter.html', {'personnel': objperso})
    return render(request, 'GestionPersonnel/ajouter.html', {'services': services, 'grades': grades, 'fonctions': fonctions,
                                                             'echellons': echellons, 'statutgrades': statutgrades,
                                                             'entites': entites, 'pashaliks': pashaliks,
                                                             'districts': districts, 'divisions': divisions, 'cercles': cercles})



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
        statut = request.POST["statut"]

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
        objperso2.statut = statut
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
def reafectation(request):

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
    personnels = Personnel.objects.all()

    if request.method == 'POST':
        objperso = Personnel.objects.get(request.POST.get("personnel"))
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

                objperso.organisme = "pashalik"
                objperso.save()

            elif((request.POST.get('districtpashalik', None) == "Cercle")):
                caidat = request.POST["caida"]
                datecaidat = request.POST["datecaida"]
                objcaidat = Caidat(idcaidat=caidat)
                objcaidatperso = Caidatpersonnel.objects.create(idpersonnel_field=objperso, idcaidat_field=objcaidat, dateaffectation=datecaidat)
                objcaidatperso.save()

                objperso.organisme = "Caida"
                objperso.save()
    return render(request, 'GestionPersonnel/reaffectation.html',{'services': services, 'grades': grades, 'fonctions': fonctions,
                                                             'echellons': echellons, 'statutgrades': statutgrades,
                                                             'entites': entites, 'pashaliks': pashaliks,
                                                             'districts': districts, 'divisions': divisions, 'cercles': cercles, 'personnels': personnels })

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
    empName = str(personnel.nomfr + " " + personnel.prenomfr)
    cin = str(personnel.cin)
    grade="ingenieur"
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
    response['Content-Disposition'] = ' filename="mypdf.pdf"'
    ##response.TransmitFile(pathtofile);
    return (response)


@login_required(login_url='/connexion')
def printpdf(req,id):
   personnel = Personnel.objects.get(idpersonnel=id)
   empName=str(personnel.nomfr+" "+personnel.prenomfr)
   cin=str(personnel.cin)
   num=str(personnel.numerofinancier)
   grade="ingenieur"
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
   pdf.text(25,138,txt="Titulaire de la C.N.I      :          "+cin)
   pdf.text(25,146,txt="P.P.R                           :          "+num)
   pdf.text(25,160,txt="Exerce à la Wilaya de la Région de l'Oriental,Préfecture d'Oujda-Angad")
   pdf.text(25,170,txt="En qualité de                :         Technicien Spécialisé ")
   pdf.text(25,185,txt="En foi de quoi,la présente attestation est délivrée à l'intéressé(e) pour servir et voir ce que de droit ")
   pdf.text(125, 200, txt="Oujda le :")
   ##pdf.cell(80)
   ##pdf.cell(60,10,'Attestation de Travaille',1,1,'C');
   pdf.output("test.pdf")
   pdfr = pdf.output(dest='S').encode('latin-1')
   response = HttpResponse(pdfr, content_type='application/pdf')
   response['Content-Disposition'] = ' filename="mypdf.pdf"'
   ##response.TransmitFile(pathtofile);
   return (response)

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
        departretraiteonecount.append(Personnel.objects.filter(administrationapp='one').filter(dateparrainageretraite__year=date).filter(dateparrainageretraite__month=i + 1).count())
        departretraitetwocount.append(Personnel.objects.filter(administrationapp='two').filter(dateparrainageretraite__year=date).filter(dateparrainageretraite__month=i + 1).count())
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
    administrationOne = Personnel.objects.filter(administrationapp='one').count()
    administrationTwo = Personnel.objects.filter(administrationapp='two').count()

    # dates 5 retraites
    i = 0
    cinqdepartretraite = []
    while i < 5:
        data = {'cinqdepartretraite' : Personnel.objects.filter(dateparrainageretraite__year=datetime.datetime.now().year - i).count(),
                'an' : datetime.datetime.now().year + i,
                'cinqdepartretraiteone': Personnel.objects.filter(administrationapp='one').filter(dateparrainageretraite__year=datetime.datetime.now().year + i).count(),
                'cinqdepartretraitetwo' : Personnel.objects.filter(administrationapp='two').filter(dateparrainageretraite__year=datetime.datetime.now().year + i).count()
                }
        cinqdepartretraite.append(data)
        i = i + 1

    #date1
    departretraiteone = []
    i = 0
    while i <= 11:
        departretraiteone.append(Personnel.objects.filter(administrationapp='one').filter(
            dateparrainageretraite__year=datetime.datetime.now().year).filter(dateparrainageretraite__month=i+1).count())
        i = i + 1

    #date2
    departretraitetwo = []
    i = 0
    while i<=11:
        departretraitetwo.append(Personnel.objects.filter(administrationapp='two').filter(
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


