from io import BytesIO
import base64
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from .models import Personnel,ParametrageRetraite
from django.db.models import Q

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def calculate_age(data):
    born = datetime.strptime(data, '%Y-%m-%d')
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def count_age_int(sexe):
    objpersonnels = Personnel.objects.all()
    for item in objpersonnels:
        item.age = calculate_age(str(item.datenaissance.date()))
        item.dateparrainageretraite = dateRetraiteCalc(str(item.datenaissance.date()))
        item.save()
    age = []
    i = 20
    while i <= 60:
        data1 = Q(age__lte=i + 4)
        data2 = Q(age__gte=i)
        age.append(Personnel.objects.filter(sexe=sexe).filter(data1 & data2).count())
        i = i + 5
    return age

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dateRetraiteCalc(daten):
    date1 = datetime.fromisoformat(daten)
    year = ParametrageRetraite.objects.all().last().nbannee
    month = ParametrageRetraite.objects.all().last().nbmois
    if month is not None:
        dateretraite = date1 + timedelta(days=(year * 365 + month * 30))
    else:
        dateretraite = date1 + timedelta(days=year * 365)
    return dateretraite