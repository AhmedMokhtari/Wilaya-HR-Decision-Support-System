
from .models import DateElimine, Conge
import numpy as np
from datetime import date, datetime

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def CalculateYearConge(typeconge,personnel):
    conges = Conge.objects.filter(type_conge=typeconge,
                                   idpersonnel_field=personnel.first(),
                                   dateretour__year=date.today().year)
    dateelimine = DateElimine.objects.all()
    listnbjours = []
    for item in conges:
        a1 = datetime.strptime(str(item.dateretour.strftime('%Y/%m/%d')), "%Y/%m/%d")
        a2 = date(date.today().year, 1, 1)
        data = [s.dateelimine.date() for s in dateelimine]
        print(np.busday_count(a2, a1.date(), holidays=data))
        listnbjours.append(np.busday_count(a2, a1.date(), holidays=data))
    return sum(listnbjours)