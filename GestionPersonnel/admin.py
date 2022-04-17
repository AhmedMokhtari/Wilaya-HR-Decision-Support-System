from django.contrib import admin
from .models import Personnel, Fonction, Fonctionpersonnel, Echelle, Echellon, Grade, Gradepersonnel, Concours, Conjoint, Conjointpersonnel

# Register your models here.
admin.site.register(Personnel)
admin.site.register(Fonction)
admin.site.register(Grade)
admin.site.register(Gradepersonnel)
admin.site.register(Echelle)
admin.site.register(Echellon)
admin.site.register(Concours)
admin.site.register(Conjoint)
admin.site.register(Conjointpersonnel)
