from django.contrib import admin
from .models import Personnel, Fonction, \
    Fonctionpersonnel, Echelle, Echellon, \
    Grade, Gradepersonnel, Concours, \
    Conjoint, Conjointpersonnel, \
    Service, Servicepersonnel, \
    Division, Enfant, Diplome

# Register your models here.
admin.site.register(Personnel)
admin.site.register(Fonction)
admin.site.register(Grade)
admin.site.register(Gradepersonnel)
admin.site.register(Concours)
admin.site.register(Conjoint)
admin.site.register(Conjointpersonnel)
admin.site.register(Servicepersonnel)
admin.site.register(Service)
admin.site.register(Division)
admin.site.register(Enfant)
admin.site.register(Diplome)
admin.site.register(Fonctionpersonnel)
admin.site.register(Echelle)
admin.site.register(Echellon)