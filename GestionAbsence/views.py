from django.shortcuts import render
from .models import Personnel, Absence
from django.db.models import Q
# Create your views here.
def taboardabsence(request):
    absence=Absence.objects.all()
    totalabsence=absence.count()
    daySum=sum(absence.values_list('nbjours', flat=True))
    criterionH = Q(sexe="Homme-ذكر")
    criterionF = Q(sexe="Femme-أنثى")
    criterion = Q(idpersonnel__in=Absence.objects.values_list('idpersonnel_field', flat=True))
    hommes = Personnel.objects.filter(criterion & criterionH).count()
    femmes = Personnel.objects.filter(criterion & criterionF).count()
    justifier=Absence.objects.filter(justification=1).count()
    nojustifier=Absence.objects.filter(justification=0).count()
    ##hommes = perso[sexe=='Homme-ذكر'].count()
    cont={
        'totalabsence':totalabsence,
        'daySum':daySum,
        'femmes':femmes,
        'hommes':hommes,
        'justifier':justifier,
        'nojustifier': nojustifier,

    }
    return render(request,'GestionAbsence/tboard.html',cont)
def absence(request):
    info = { 'Absence' : Absence.objects.all(),'personnels' : Personnel.objects.all()}
    return render(request, 'GestionAbsence/ajouter.html',info)
def ajouterabsence(request):
        id=request.POST.get("Personnel",False)
        id=id.split("-")
        #objperso = Personnel(cin=str(id[0]))
        obj=Personnel.objects.get(cin=str(id[0]))
        nbjours = request.POST.get("nbJours",False)
        motif = request.POST.get("motif",False)
        dateabsence = request.POST.get("dateab",False)
        justification=request.POST.get("justification",False)
        objectab=Absence.objects.create(dateabsence=dateabsence,nbjours=str(nbjours),motif=motif,justification=justification,idpersonnel_field=obj)
        objectab.save()
        info = {'Absence': Absence.objects.all(), 'personnels': Personnel.objects.all()}
        return render(request, 'GestionAbsence/ajouter.html', info)
def export_abs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Absence.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Full Name','DateAbsence','Nb Jours','Motif'])
    Absencs = Absence.objects.all().values_list('idpersonnel_field','dateabsence','nbjours','motif')
    for abs in Absencs:
        writer.writerow(abs)
    return response
def modifierabs(request,id):
    obj = { 'personnels' : Personnel.objects.all(),'abs':Absence.objects.get(idabsence=id)}
    return render(request, 'GestionAbsence/modifier.html',obj)
def modifierabsence(request,id):
    nbjours = request.POST.get("nbJours", False)
    motif = request.POST.get("motif", False)
    dateabsence = request.POST.get("dateab", False)
    objectab = Absence.objects.get(idabsence=id)
    objectab.dateabsence=dateabsence
    objectab.nbjours=str(nbjours)
    objectab.motif=motif
    objectab.save()
    return render(request, 'GestionAbsence/absence.html')
