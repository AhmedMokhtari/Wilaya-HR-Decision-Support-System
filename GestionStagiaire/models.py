from django.db import models
from GestionPersonnel.models import *

# Create your models here.

class Stage(models.Model):
    idstage = models.AutoField(db_column='IdStage', primary_key=True)
    nomstagiairear = models.CharField(db_column='NomStagiaireAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomstagiairear = models.CharField(db_column='PrenomStagiaireAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomstagiairefr = models.CharField(db_column='NomStagiaireFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomstagiairefr = models.CharField(db_column='PrenomStagiaireFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    idservice_field = models.ForeignKey(Service, models.DO_NOTHING, db_column='IdService#', blank=True, null=True)
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    sexe = models.CharField(db_column='Sexe', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=40, db_collation='French_CI_AS', blank=True, null=True)
    tele = models.CharField(db_column='Tele', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    datedebutstage = models.DateTimeField(db_column='DateDebutStage', blank=True, null=True)
    nbmois = models.IntegerField(db_column='Nbmois', blank=True, null=True)
    datefinstage = models.DateTimeField(db_column='DateFinStage', blank=True, null=True)
    cinpdf = models.FileField(db_column='Cinpdf', upload_to='')
    cvpdf = models.FileField(db_column='CVpdf', upload_to='')
    demandepdf = models.FileField(db_column='Demandepdf', upload_to='')
    assurancepdf = models.FileField(db_column='Assurancepdf', upload_to='')

    class Meta:
        managed = False
        db_table = 'Stage'


class ServiceStage(models.Model):
    idservicestage = models.AutoField(db_column='IdServiceStage', primary_key=True)
    idservice_field = models.ForeignKey('GestionPersonnel.Service', models.DO_NOTHING, db_column='IdService#', blank=True, null=True)
    idstage_field = models.ForeignKey(Stage, models.DO_NOTHING, db_column='IdStage#', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ServiceStage'

class PashalikStage(models.Model):
    idpashalikstage = models.AutoField(db_column='IdPashalikStage', primary_key=True)
    idpashalik_field = models.ForeignKey('GestionPersonnel.Pashalik', models.DO_NOTHING, db_column='IdPashalik#', blank=True, null=True)
    idstage_field = models.ForeignKey(Stage, models.DO_NOTHING, db_column='IdStage#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PashalikStage'

class AnnexeStage(models.Model):
    idannexestage = models.AutoField(db_column='IdAnnexeStage', primary_key=True)
    idannexe_field = models.ForeignKey('GestionPersonnel.Annexe', models.DO_NOTHING, db_column='IdAnnexe#', blank=True, null=True)
    idstage_field = models.ForeignKey(Stage, models.DO_NOTHING, db_column='IdStage#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AnnexeStage'

class CaidatStage(models.Model):
    idcaidatstage = models.AutoField(db_column='IdAnnexeStage', primary_key=True)
    idcaidat_field = models.ForeignKey('GestionPersonnel.Caidat', models.DO_NOTHING, db_column='IdCaidat#', blank=True, null=True)
    idstage_field = models.ForeignKey(Stage, models.DO_NOTHING, db_column='IdStage#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CaidatStage'