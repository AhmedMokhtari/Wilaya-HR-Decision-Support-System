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


class Avencement(models.Model):
    iavencement = models.AutoField(db_column='IAvencement', primary_key=True)
    idgrade_field = models.ForeignKey('GestionPersonnel.Grade', models.DO_NOTHING, db_column='IdGrade#', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('GestionPersonnel.Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)
    changementdegrade = models.CharField(db_column='ChangementDeGrade', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    idechellon_field = models.ForeignKey('GestionPersonnel.Echellon', models.DO_NOTHING, db_column='idEchellon#', blank=True, null=True)
    indice = models.CharField(db_column='Indice', max_length=15, db_collation='French_CI_AS', blank=True, null=True)
    dateechellon = models.DateTimeField(db_column='DateEchellon', blank=True, null=True)
    changementdechellon = models.CharField(db_column='ChangementDEchellon', max_length=100, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Avencement'


class Rythme(models.Model):
    idrythme = models.AutoField(db_column='IdRythme', primary_key=True)  # Field name made lowercase.
    idgrade_field = models.ForeignKey('GestionPersonnel.Grade', models.DO_NOTHING, db_column='IdGrade#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    echellondebut = models.ForeignKey('GestionPersonnel.Echellon', models.DO_NOTHING, db_column='EchellonDebut', blank=True, null=True, related_name="Rythme")
    echellonfin = models.ForeignKey('GestionPersonnel.Echellon', models.DO_NOTHING, db_column='EchellonFin', blank=True, null=True)
    rapide = models.IntegerField(db_column='Rapide', blank=True, null=True)  # Field name made lowercase.
    moyen = models.IntegerField(db_column='Moyen', blank=True, null=True)  # Field name made lowercase.
    lent = models.IntegerField(db_column='Lent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rythme'
