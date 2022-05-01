from io import BytesIO
import base64
import matplotlib.pyplot as plt
from datetime import datetime
from .models import Personnel
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
    born  = datetime.strptime(data, '%Y-%m-%d')
    print(born)
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def count_age_int(sexe):
    age = []
    i = 20
    while i <= 60:
        data1 = Q(age__lte=i + 4)
        data2 = Q(age__gte=i)
        age.append(Personnel.objects.filter(sexe=sexe).filter(data1 & data2).count())
        i = i + 5
    return age