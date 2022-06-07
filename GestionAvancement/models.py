from django.db import models

# Create your models here.
class Notation(models.Model):
    idnotation = models.AutoField(db_column='IdNotation', primary_key=True)
    note = models.IntegerField(db_column='Note', blank=True, null=True)
    annee = models.IntegerField(db_column='Annee', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('GestionPersonnel.Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notation'


