from django.db import models

# Create your models here.

# -------------------------------------------------------
class Personnel(models.Model):
    idpersonnel = models.AutoField(db_column='IdPersonnel', primary_key=True)  # Field name made lowercase.
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)  # Field name made lowercase.
    lieunaissancear = models.CharField(db_column='LieuNaissanceAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lieunaissancefr = models.CharField(db_column='LieuNaissanceFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adressear = models.CharField(db_column='AdresseAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    adressefr = models.CharField(db_column='AdresseFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=40, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tele = models.IntegerField(db_column='Tele', blank=True, null=True)  # Field name made lowercase.
    situationfamilialear = models.CharField(db_column='SituationFamilialeAr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    situationfamilialefr = models.CharField(db_column='SituationFamilialeFr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sexe = models.CharField(db_column='Sexe', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    vaccination = models.BooleanField(db_column='Vaccination', blank=True, null=True)  # Field name made lowercase.
    numerolocation = models.CharField(db_column='NumeroLocation', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    numerofinancier = models.CharField(db_column='NumeroFinancier', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    daterecrutement = models.DateTimeField(db_column='DateRecrutement', blank=True, null=True)  # Field name made lowercase.
    datedemarcation = models.DateTimeField(db_column='DateDemarcation', blank=True, null=True)  # Field name made lowercase.
    dateparrainageretraite = models.DateTimeField(db_column='DateParrainageRetraite', blank=True, null=True)  # Field name made lowercase.
    cmr = models.CharField(db_column='Cmr', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    posteemploye = models.CharField(db_column='PosteEmploye', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    metier = models.CharField(db_column='Metier', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    typeemploye = models.CharField(db_column='TypeEmploye', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tachesprecedentes = models.CharField(db_column='TachesPrecedentes', max_length=60, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rib = models.IntegerField(db_column='Rib', blank=True, null=True)  # Field name made lowercase.
    ancienneteadmi = models.CharField(db_column='ancienneteAdmi', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    numcnopsaf = models.CharField(db_column='NumCnopsAf', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    numcnopsim = models.CharField(db_column='NumCnopsIm', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    administrationapp = models.CharField(db_column='AdministrationApp', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Personnel'

# -------------------------------------------------------
class Fonction(models.Model):
    idfonction = models.AutoField(db_column='IdFonction', primary_key=True)  # Field name made lowercase.
    libellefontionar = models.CharField(db_column='LibelleFontionAr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellefonctionfr = models.CharField(db_column='LibelleFonctionFr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fonction'

# -------------------------------------------------------
class Fonctionpersonnel(models.Model):
    idfonction_field = models.OneToOneField(Fonction, models.DO_NOTHING, db_column='IdFonction#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    datefonction = models.DateTimeField(db_column='DateFonction')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FonctionPersonnel'
        unique_together = (('idfonction_field', 'datefonction'),)


# -------------------------------------------------------
class Concours(models.Model):
    idconcours = models.AutoField(db_column='IdConcours', primary_key=True)  # Field name made lowercase.
    libelleconcoursar = models.CharField(db_column='LibelleConcoursAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleconcoursfr = models.CharField(db_column='LibelleConcoursFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateconcours = models.DateTimeField(db_column='DateConcours', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Concours'

# -------------------------------------------------------
class Echelle(models.Model):
    idechelle = models.AutoField(db_column='IdEchelle', primary_key=True)  # Field name made lowercase.
    echelle = models.IntegerField(db_column='Echelle', blank=True, null=True)  # Field name made lowercase.
    dateechelle = models.DateTimeField(db_column='DateEchelle', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Echelle'

# -------------------------------------------------------
class Echellon(models.Model):
    idechellon = models.AutoField(db_column='IdEchellon', primary_key=True)  # Field name made lowercase.
    echellon = models.CharField(db_column='Echellon', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateechellon = models.DateTimeField(db_column='DateEchellon', blank=True, null=True)  # Field name made lowercase.
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='IdEchelle#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Echellon'

# -------------------------------------------------------
class Grade(models.Model):
    idgrade = models.AutoField(db_column='IdGrade', primary_key=True)  # Field name made lowercase.
    gradear = models.CharField(db_column='GradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gradefr = models.CharField(db_column='GradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)  # Field name made lowercase.
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='IdEchelle#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Grade'

# -------------------------------------------------------
class Gradepersonnel(models.Model):
    idgrade_field = models.OneToOneField(Grade, models.DO_NOTHING, db_column='IdGrade#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)  # Field name made lowercase.
    changementdegrade = models.CharField(db_column='ChangementDeGrade', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idconcours_field = models.ForeignKey(Concours, models.DO_NOTHING, db_column='IdConcours#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'GradePersonnel'
        unique_together = (('idgrade_field', 'idpersonnel_field'),)

