from django.shortcuts import render,redirect
from .models import Personnel,Conjoint, Conjointpersonnel, \
    Service, Servicepersonnel, Grade, \
    Gradepersonnel, Enfant, Diplome, Fonction, Fonctionpersonnel

from django.contrib.auth.decorators import login_required
from fpdf import FPDF
from django.http import HttpResponse
import os


#personnel -------------------------------.
@login_required(login_url='/connexion')
def consultation(request):
    personnels = { 'personnels' : Personnel.objects.all()}
    return render(request, 'GestionPersonnel/consultation.html', personnels)


@login_required(login_url='/connexion')


def ajouter(request):

    services = Service.objects.all()
    grades = Grade.objects.all()
    fonctions = Fonction.objects.all()
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
        situatfr = request.POST["situationffr"]
        situatar = request.POST["situationfar"]
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
        photo = request.POST["photo"]
        dateservice = request.POST["dateservice"]
        dategrade = request.POST["dategrade"]
        service = request.POST["service"]
        grade = request.POST["grade"]
        fonction = request.POST["fonction"]
        datefonction = request.POST["datefonction"]

        objperso= Personnel(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr,
                            lieunaissancear=lieunar, lieunaissancefr=lieunfr, datenaissance=daten,
                            tele=tele, email=email, situationfamilialefr=situatfr, adressear=adressear,
                            adressefr=adressefr, numerofinancier=numiden, daterecrutement=daterec,
                            datedemarcation=datedec, dateparrainageretraite=dateretr, numcnopsaf=numcnopsaf,
                            numcnopsim=numcnopsim, rib=rib, ancienneteadmi=ancadmi, administrationapp=adminiapp,
                            situationfamilialear=situatar, photo=photo)
        objperso.save()

        objservice = Service(idservice=service)
        objgrade = Grade(idgrade=grade)
        objfonction = Fonction(idfonction=fonction)

        objfonctionperso = Fonctionpersonnel(idpersonnel_field=objperso, idfonction_field=objfonction, datefonction=datefonction)
        objserviceperso = Servicepersonnel(idpersonnel_field=objperso, idservice_field=objservice, dateaffectation=dateservice)
        objgradeperso = Gradepersonnel(idpersonnel_field=objperso, idgrade_field=objgrade, dategrade=dategrade)

        objfonctionperso.save()
        objserviceperso.save()
        objgradeperso.save()

        conjoints = Conjointpersonnel.objects.filter(idpersonnel_field=objperso.idpersonnel).all()

        return render(request, 'GestionPersonnel/ajouter.html', {'personnel': objperso})
    else:
        return render(request, 'GestionPersonnel/ajouter.html', {'services': services, 'grades': grades ,'fonctions':fonctions})


@login_required(login_url='/connexion')
def modifier(request, id):
    personnel = Personnel.objects.get(idpersonnel=id)
    conjointsinperso = Conjointpersonnel.objects.filter(idpersonnel_field=id)
    conjoints = Conjoint.objects.filter(idconjoint__in=conjointsinperso.values_list('idconjoint_field', flat=True))
    serviceperso = Servicepersonnel.objects.filter(idpersonnel_field=id).values_list('idservice_field', flat=True)
    servicelast = Service.objects.filter(idservice__in=serviceperso).last()

    services = Service.objects.all()
    grades = Grade.objects.all()

    if request.method == 'POST':
        tele = request.POST["tele"]
        email = request.POST["email"]
        situatar = request.POST.get('situationfar', False)
        adressear = request.POST["adressear"]
        adressefr = request.POST["adressefr"]
        nummatri = request.POST["nummatri"]
        numiden = request.POST["numiden"]
        personnel = Personnel.objects.get(idpersonnel=id)
        personnel.save()

    return render(request, 'GestionPersonnel/modifier.html',
                      {'personnel': personnel, 'conjoints': conjoints, 'services': services, 'grades': grades, 'servicelast': servicelast})





#conjoint -----------------------------------
@login_required(login_url='/connexion')
def conjoint(request):
    if request.method == 'POST':
        nomfr = request.POST["nomfr"]
        nomar = request.POST["nomar"]
        prenomfr = request.POST["prenomfr"]
        prenomar = request.POST["prenomar"]
        cin = request.POST["cin"]
        daten = request.POST["daten"]
        lieun = request.POST["lieun"]
        personnelcin = request.POST["personnelcin"]
        obj1 = Conjoint(nomar=nomar, nomfr=nomfr, cin=cin, prenomar=prenomar, prenomfr=prenomfr, lieunaissance=lieun, datenaissance=daten)
        obj1.save()

        pers = Personnel.objects.filter(cin=personnelcin).first()
        con = Conjoint.objects.filter(cin=cin).first()
        obj2 = Conjointpersonnel(idconjoint_field=con, idpersonnel_field=pers)
        obj2.save()

    else:
        cinpersonnel = request.GET.get('personnel', None)
        if(cinpersonnel) :
            return render(request, 'GestionPersonnel/conjoint.html', {'personnel': cinpersonnel})
        else:
            return render(request, 'GestionPersonnel/conjoint.html')
    if(obj1)  :
        return render(request, 'GestionPersonnel/conjoint.html', {'conjoint' : obj1 ,'personnel': pers.cin})
    else:
        return render(request, 'GestionPersonnel/conjoint.html')



#enfant -----------------------------------
@login_required(login_url='/connexion')
def enfant(request):
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
        return render(request, 'GestionPersonnel/enfant.html', {'enfant': Enfant.objects.all(),'personnel': cinpersonnel, 'conjoints':conjoints})

    return render(request, 'GestionPersonnel/enfant.html', {'personnel': cinpersonnel, 'conjoints':conjoints})


#diplome -----------------------------------
@login_required(login_url='/connexion')
def diplome(request):
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
        return render(request, 'GestionPersonnel/diplome.html', {'personnel': cinpersonnel, 'diplome':objdiplome})

    return render(request, 'GestionPersonnel/diplome.html', {'personnel': cinpersonnel})




def printpdfquitter(req):
    empName = "Ahmed Mokhtari";
    cin = "FB129386"
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
    return (response) ;



def printpdf(req):
   empName="Ahmed Mokhtari";
   cin="FB129386"
   num="123823"
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

#taboard------------------------------------------------------
@login_required(login_url='/connexion')
def taboardpersonnel(request):
    return render(request,'GestionPersonnel/tboardpersonnel.html',)

