from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class PersonnelImportExport(ImportExportModelAdmin):
    pass

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['nomar', 'prenomar', 'cin','age']
    list_display_links =  ['nomar', 'prenomar', 'age']
    search_fields = ['nomar', 'prenomar', 'cin', 'age']

class GradeAdmin(admin.ModelAdmin):
    list_display = ['gradear', 'gradefr', 'idstatutgrade_field','idechelle_field']
    list_display_links =  ['gradear', 'gradefr', 'idstatutgrade_field','idechelle_field']
    search_fields = ['gradear', 'gradefr', 'idstatutgrade_field','idechelle_field']

admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Fonction)
admin.site.register(ParametrageRetraite)
admin.site.register(Grade, GradeAdmin)
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
admin.site.register(Caidat)
admin.site.register(Cercle)
admin.site.register(Caidatpersonnel)
admin.site.register(Statutgrade)
admin.site.site_header = "ولاية جهة الشرق"
admin.site.site_title = "ولاية جهة الشرق"

