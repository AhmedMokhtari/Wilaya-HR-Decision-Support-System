
from .models import *
import numpy as np
from datetime import date, datetime, timedelta

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def CalculateYearConge(typeconge,personnel):
    conges = Conge.objects.filter(type_conge=typeconge,
                                   idpersonnel_field=personnel.first(),
                                   dateretour__year=date.today().year)
    listnbjours = []
    for item in conges:
        listnbjours.append(item.nbjour)
    return sum(listnbjours)


def findWorkingDayAfter(startDate, daysToAdd):
    dateelimine = DateElimine.objects.all()
    data = [s.dateelimine.strftime('%Y/%m/%d') for s in dateelimine]
    workingDayCount = 0
    while workingDayCount < daysToAdd:
        startDate += timedelta(days=1)
        weekday = int(startDate.strftime('%w'))
        if (weekday != 0 and weekday != 6 and startDate.strftime('%Y/%m/%d') not in data):
            workingDayCount += 1

    return startDate