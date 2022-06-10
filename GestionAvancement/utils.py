from GestionPersonnel.models import *
from .models import *
from datetime import datetime
def yearempty(listpersoid):
    listPerso=[]
    for id in listpersoid:
        notationAnnee = Notation.objects.filter(idpersonnel_field=id).values_list('annee', flat=True)
        perso = Personnel.objects.get(idpersonnel=id)
        dateDemarationYear = datetime.strptime(str(perso.datedemarcation), '%Y-%m-%d %H:%M:%S%z')
        yearNow = datetime.now().year
        listyearempty = []
        listyear = []
        for a in range(dateDemarationYear.year, yearNow + 1):
            listyear.append(a)
        for a in listyear:
            if a not in list(notationAnnee):
                listyearempty.append(a)
        for year in listyearempty:
            persoinfo={'name':perso.prenomar+' '+perso.nomar,'year':year,'id':perso.idpersonnel,'cin':perso.cin}
            listPerso.append(persoinfo)
    return listPerso
def indice(gradeid):
    grade = Grade.objects.get(idgrade=gradeid)
    statutgrade = Statutgrade.objects.filter(idstatutgrade=grade.idstatutgrade_field.idstatutgrade).first()
    indice = []
    if (statutgrade.statutgradefr == 'Administrateurs MI'):
        if (grade.idechelle_field.echelle == '10'):
            indice = ['275', '300', '329', '355', '380', '402', '428', '460', '484', '512', '564']
        elif (grade.idechelle_field.echelle == '11'):
            indice = ['336', '369', '406', '436', '476', '509', '542', '578', '610', '639', '704']
        else:
            indice = ['704', '746', '779', '812', '840', '870']
    elif (statutgrade.statutgradefr == 'Administrateurs AC'):
        if (grade.idechelle_field.echelle == '10'):
            indice = ['275', '300', '326', '351', '377', '402', '428', '456', '484', '512', '564']
        elif (grade.idechelle_field.echelle == '11'):
            indice = ['336', '369', '403', '436', '472', '509', '542', '574', '606', '639', '704']
        else:
            indice = ['704', '746', '779', '812', '840', '870']
    elif (statutgrade.statutgradefr == "Ingénieurs et Architectes"):
        if (grade.gradefr == "Ingénieur d'Etat 1er grade" or grade.gradefr == "Architecte 1er grade"):
            indice = ['336', '369', '403', '436', '472']
        elif (grade.gradefr == "Ingénieur d'application 1er grade"):
            indice = ['275', '300', '326', '351', '377']
        elif (grade.gradefr == "Architecte en chef grade principal" or grade.gradefr == "Ingénieur d'Etat grade principal"):
            indice = ['870', '900', '930', '960', '990']
        elif (grade.gradefr == "Ingénieur d'Etat grade principal" or grade.gradefr == "Architecte grade principal"):
            indice = ['509', '542', '574', '606', '639', '704']
        elif (grade.gradefr == "Ingénieur en chef 1er grade" or grade.gradefr == "Architecte en chef 1er grade"):
            indice = ['704', '746', '779', '812', '840', '870']
        elif (grade.gradefr == "Ingénieur d'application grade principal"):
            indice = ['402', '428', '456', '484', '512', '564']
    elif (statutgrade.statutgradefr == "Techniciens" or statutgrade.statutgradefr == "Rédacteurs"):
        if (grade.idechelle_field.echelle == "8"):
            indice = ['207', '224', '241', '259', '276', '293', '311', '332', '353', '373']
        elif (grade.idechelle_field.echelle == "9"):
            indice = ['235', '253', '274', '296', '317', '339', '361', '382', '404', '438']
        elif (grade.idechelle_field.echelle == "10"):
            indice = ['275', '300', '326', '351', '377', '402', '428', '456', '484', '512', '564']
        elif (grade.idechelle_field.echelle == "11"):
            indice = ['336', '369', '403', '436', '472', '509', '542', '574', '606', '639', '675', '704', '690', '704']
    elif (statutgrade.statutgradefr == "Adjoints Administratifs" or statutgrade.statutgradefr == "Adjoints Techniques"):
        if (grade.idechelle_field.echelle == "8"):
            indice = ['207', '224', '241', '259', '276', '293', '311', '332', '353', '373']
        elif (grade.idechelle_field.echelle == "7"):
            indice = ['177', '193', '208', '225', '242', '260', '277', '291', '305', '318']
        elif (grade.idechelle_field.echelle == "6"):
            indice = ['153', '161', '173', '185', '197', '209', '222', '236', '249', '262']
        elif (grade.idechelle_field.echelle == "5"):
            indice = ['137', '141', '150', '157', '165', '174', '183', '192', '201', '220']
    return indice