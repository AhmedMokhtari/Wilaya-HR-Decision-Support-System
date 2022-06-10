import datetime
from django.core import serializers
import json
import os
from fpdf import FPDF
from django.db import connection
import arabic_reshaper
from bidi.algorithm import get_display
from pathlib import Path
from operator import itemgetter
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


def pdfavencement(request):
    grade = Grade.objects.get(idgrade=1)
    annee = str(datetime.datetime.now().year)
    decision1 = 'يترقى'
    decision2 = 'يترقى'
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
    pdf.cell(17,24,txt=get_display(arabic_reshaper.reshape('ملاحظات')),border=1,align='C',fill=True)
    #pdf.set_x(35)
    pdf.multi_cell(22,12,txt=get_display(arabic_reshaper.reshape(' المتساوية الأعضاء   رأي اللجنة الإدارية')),border=1,align='C',fill=True)
    pdf.set_y(85)
    pdf.set_x(39)
    pdf.cell(69,12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية الجديدة درجة {grade.gradear}')),border=1,align='C',fill=True,ln=2)
    pdf.cell(34,12,txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')),border=1,fill=True,align='C')
    pdf.cell(24,12,txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')),border=1,fill=True,align='C')
    pdf.cell(11,12,txt=get_display(arabic_reshaper.reshape('الرتبة')),border=1,fill=True,align='C',ln=2)
    pdf.set_y(85)
    pdf.set_x(108)
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النقطة')),border=1,fill=True,align='C')
    pdf.cell(12,24,txt=get_display(arabic_reshaper.reshape('النسق')),border=1,fill=True,align='C')
    pdf.cell(69, 12,txt=get_display(arabic_reshaper.reshape(f'الوضعية الإدارية القديمة درجة {grade.gradear}')), border=1,align='C', fill=True, ln=2)
    pdf.cell(34, 12, txt=get_display(arabic_reshaper.reshape('تاريخ الفعالية في الرتبة')),border=1, fill=True, align='C')
    pdf.cell(24, 12, txt=get_display(arabic_reshaper.reshape('الرقم الاستدلالي')), border=1,fill=True, align='C')
    pdf.cell(11, 12, txt=get_display(arabic_reshaper.reshape('الرتبة')), border=1, fill=True,align='C', ln=2)
    pdf.set_y(85)
    pdf.set_x(201)
    pdf.cell(19,24, txt="Nom",border=1,fill=True,align='C')
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

    grades = Grade.objects.get(idgrade=1)
    personnels = Personnel.objects.all()
    listoutput = []
    for item in personnels:
        objgradepersonnel = Gradepersonnel.objects.filter(idpersonnel_field=item)
        if (objgradepersonnel.last() != None and objgradepersonnel.last().idgrade_field == grades):
            listoutput.append(objgradepersonnel.last())

    for item2 in listoutput:
        objrythme = Rythme.objects.filter(echellondebut=item2.idechellon_field,
                                          idgrade_field=item2.idgrade_field).first()
        date = item2.dateechellon + datetime.timedelta(30 * objrythme.rapide)
        note = Notation.objects.filter(idpersonnel_field=item2.idpersonnel_field, annee__lte=date.year,
                                       annee__gte=item2.dateechellon.year)
        listnote = []
        for item3 in note:
            listnote.append(item3.note)
        moyenne = sum(listnote) / len(listnote)
        mois = 1
        if (item2.idgrade_field.gradefr == 'Administrateur adjoint' or item2.idgrade_field.gradefr == 'Administrateur'):
            if (item2.idechellon_field == '6' or item2.idechellon_field == '10'):
                mois = 1
            else:
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
            if (moyenne >= 16 and moyenne <= 20):
                mois = objrythme.rapide
            elif (moyenne >= 10 and moyenne <= 16):
                mois = objrythme.moyen
            elif (moyenne < 10):
                mois = objrythme.lent

        datefin = item2.dateechellon + datetime.timedelta(30 * mois)
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