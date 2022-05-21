from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
#admin.site.register(Personnel)
@admin.register(Personnel)
class PersonnelImportExport(ImportExportModelAdmin):
    pass
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
admin.site.register(Entite)
admin.site.register(Annexe)
admin.site.register(Pashalik)
admin.site.register(District)