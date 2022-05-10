from django.db import models

class Absence(models.Model):
    idabsence = models.AutoField(db_column='IdAbsence', primary_key=True)  # Field name made lowercase.
    dateabsence = models.DateTimeField(db_column='DateAbsence', blank=True, null=True)  # Field name made lowercase.
    nbjours = models.IntegerField(db_column='NbJours', blank=True, null=True)  # Field name made lowercase.
    motif = models.CharField(db_column='Motif', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    justification = models.BooleanField(db_column='Justification')
    idpersonnel_field = models.ForeignKey('GestionPersonnel.Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Absence'

