from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Conge, DateElimine
from GestionPersonnel.models import Personnel, Service, Servicepersonnel, Division
from datetime import datetime
import numpy as np
from django.db import connection

# Create your views here.
@login_required(login_url='/connexion')
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
        perso = Personnel.objects.filter(idpersonnel=request.POST.get('perso')).first()
        datedecom = request.POST.get("datedecon")
        typede = request.POST["typede"]
        datere = request.POST.get('datere')
        a1 = datetime.strptime(datedecom, "%Y-%m-%d")
        a2 = datetime.strptime(datere, "%Y-%m-%d")
        data = [s.dateelimine.date() for s in dateelimine]
        datenbjours = np.busday_count(a1.date(), a2.date(), holidays=data)
        nbjours = datenbjours
        objconge = Conge(type_conge=typede, datedebut=a1, dateretour=a2, idpersonnel_field=perso,nbjour=nbjours)
        objconge.save()
        return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'objconge': objconge, 'conges': conges, 'divisions': divisions})
    return render(request, 'GestionConge/conge.html', {'personnels': personnels, 'congepersonnel': congepersonnel, 'conges': conges, 'divisions': divisions})

@login_required(login_url='/connexion')
def delete(request,id):
    objconge = Conge.objects.get(idconge=id)
    objconge.delete()
    response = redirect('/conge/ajouterconge')
    return response
