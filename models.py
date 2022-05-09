# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Absence(models.Model):
    idabsence = models.AutoField(db_column='IdAbsence', primary_key=True)  # Field name made lowercase.
    dateabsence = models.DateTimeField(db_column='DateAbsence', blank=True, null=True)  # Field name made lowercase.
    nbjours = models.IntegerField(db_column='NbJours', blank=True, null=True)  # Field name made lowercase.
    motif = models.CharField(db_column='Motif', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    justification = models.BooleanField(db_column='Justification')
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Absence'


class Admin(models.Model):
    idadmin = models.AutoField(db_column='IdAdmin', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=12, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Concours(models.Model):
    idconcours = models.AutoField(db_column='IdConcours', primary_key=True)  # Field name made lowercase.
    libelleconcoursar = models.CharField(db_column='LibelleConcoursAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleconcoursfr = models.CharField(db_column='LibelleConcoursFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateconcours = models.DateTimeField(db_column='DateConcours', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Concours'


class Congeset(models.Model):
    idconge = models.AutoField(db_column='IdConge', primary_key=True)  # Field name made lowercase.
    type_conge = models.CharField(max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    datedebut = models.DateTimeField(db_column='dateDebut', blank=True, null=True)  # Field name made lowercase.
    nbjour = models.IntegerField(db_column='nbJour', blank=True, null=True)  # Field name made lowercase.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'CongeSet'


class Conjoint(models.Model):
    idconjoint = models.AutoField(db_column='IdConjoint', primary_key=True)  # Field name made lowercase.
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)  # Field name made lowercase.
    lieunaissance = models.CharField(db_column='LieuNaissance', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Conjoint'


class Conjointpersonnel(models.Model):
    idconjoint_field = models.OneToOneField(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ConjointPersonnel'
        unique_together = (('idconjoint_field', 'idpersonnel_field'),)


class Diplome(models.Model):
    iddiplome = models.AutoField(db_column='IdDiplome', primary_key=True)  # Field name made lowercase.
    diplomefr = models.CharField(db_column='DiplomeFr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    diplomear = models.CharField(db_column='DiplomeAr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    etablissement = models.CharField(db_column='Etablissement', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    specialitear = models.CharField(db_column='SpecialiteAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    specialitefr = models.CharField(db_column='SpecialiteFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datediplome = models.DateTimeField(db_column='DateDiplome', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Diplome'


class Diplomepersonnel(models.Model):
    iddiplome_field = models.OneToOneField(Diplome, models.DO_NOTHING, db_column='IdDiplome#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'DiplomePersonnel'
        unique_together = (('iddiplome_field', 'idpersonnel_field'),)


class Division(models.Model):
    iddivision = models.AutoField(db_column='IdDivision', primary_key=True)  # Field name made lowercase.
    libelledivisionar = models.CharField(db_column='LibelleDivisionAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelledivisionfr = models.CharField(db_column='LibelleDivisionFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Division'


class Echelle(models.Model):
    idechelle = models.AutoField(db_column='IdEchelle', primary_key=True)  # Field name made lowercase.
    echelle = models.IntegerField(db_column='Echelle', blank=True, null=True)  # Field name made lowercase.
    dateechelle = models.DateTimeField(db_column='DateEchelle', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Echelle'


class Echellon(models.Model):
    idechellon = models.AutoField(db_column='IdEchellon', primary_key=True)  # Field name made lowercase.
    echellon = models.CharField(db_column='Echellon', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateechellon = models.DateTimeField(db_column='DateEchellon', blank=True, null=True)  # Field name made lowercase.
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='IdEchelle#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Echellon'


class Enfant(models.Model):
    idenfant = models.AutoField(db_column='IdEnfant', primary_key=True)  # Field name made lowercase.
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)  # Field name made lowercase.
    lieunaissancear = models.CharField(db_column='LieuNaissanceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lieunaissancefr = models.CharField(db_column='LieuNaissanceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    lienjuridique = models.CharField(db_column='LienJuridique', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idconjoint_field = models.ForeignKey(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Enfant'


class Fonction(models.Model):
    idfonction = models.AutoField(db_column='IdFonction', primary_key=True)  # Field name made lowercase.
    libellefontionar = models.CharField(db_column='LibelleFontionAr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellefonctionfr = models.CharField(db_column='LibelleFonctionFr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Fonction'


class Fonctionpersonnel(models.Model):
    idfonction_field = models.OneToOneField(Fonction, models.DO_NOTHING, db_column='IdFonction#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    datefonction = models.DateTimeField(db_column='DateFonction')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FonctionPersonnel'
        unique_together = (('idfonction_field', 'datefonction'),)


class Grade(models.Model):
    idgrade = models.AutoField(db_column='IdGrade', primary_key=True)  # Field name made lowercase.
    gradear = models.CharField(db_column='GradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gradefr = models.CharField(db_column='GradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)  # Field name made lowercase.
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='IdEchelle#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Grade'


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


class Position(models.Model):
    idposition = models.AutoField(db_column='IdPosition', primary_key=True)  # Field name made lowercase.
    libellepositionar = models.CharField(db_column='LibellePositionAr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellepositionfr = models.CharField(db_column='LibellePositionFr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellesouspositionar = models.CharField(db_column='LibelleSousPositionAr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellesouspositionfr = models.CharField(db_column='LibelleSousPositionFr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Position'


class Positionpersonnel(models.Model):
    idposition_field = models.OneToOneField(Position, models.DO_NOTHING, db_column='IdPosition#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'PositionPersonnel'
        unique_together = (('idposition_field', 'idpersonnel_field'),)


class Service(models.Model):
    idservice = models.AutoField(db_column='IdService', primary_key=True)  # Field name made lowercase.
    libelleservicear = models.CharField(db_column='LibelleServiceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleservicefr = models.CharField(db_column='LibelleServiceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    iddivision_field = models.ForeignKey(Division, models.DO_NOTHING, db_column='IdDivision#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Service'


class Servicepersonnel(models.Model):
    idservice_field = models.OneToOneField(Service, models.DO_NOTHING, db_column='IdService#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServicePersonnel'
        unique_together = (('idservice_field', 'idpersonnel_field'),)


class Stage(models.Model):
    idstage = models.AutoField(db_column='IdStage', primary_key=True)  # Field name made lowercase.
    nomstagiairear = models.CharField(db_column='NomStagiaireAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomstagiairear = models.CharField(db_column='PrenomStagiaireAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nomstagiairefr = models.CharField(db_column='NomStagiaireFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prenomstagiairefr = models.CharField(db_column='PrenomStagiaireFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datedebutstage = models.DateTimeField(db_column='DateDebutStage', blank=True, null=True)  # Field name made lowercase.
    datefinstage = models.DateTimeField(db_column='DateFinStage', blank=True, null=True)  # Field name made lowercase.
    idservice_field = models.ForeignKey(Service, models.DO_NOTHING, db_column='IdService#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Stage'


class Thematiqueformation(models.Model):
    idthematiqueformation = models.AutoField(db_column='IdThematiqueFormation', primary_key=True)  # Field name made lowercase.
    libellethematique = models.CharField(db_column='LibelleThematique', max_length=70, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ThematiqueFormation'


class Thematiqueformationpersonnel(models.Model):
    idthematiqueformation_field = models.OneToOneField(Thematiqueformation, models.DO_NOTHING, db_column='IdThematiqueFormation#', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    duree = models.IntegerField(db_column='Duree', blank=True, null=True)  # Field name made lowercase.
    presence = models.BooleanField(db_column='Presence', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ThematiqueFormationPersonnel'
        unique_together = (('idthematiqueformation_field', 'idpersonnel_field'),)

class DateElimine(models.Model):
    ideateelimine= models.AutoField(db_column='IdDateElimine', primary_key=True)
    motif = models.CharField(db_column='Motif', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    dateelimine = models.DateTimeField(db_column='DateElimine', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DateElimine'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='French_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='French_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='French_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='French_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='French_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='French_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='French_CI_AS')
    email = models.CharField(max_length=254, db_collation='French_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='French_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='French_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='French_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='French_CI_AS')
    model = models.CharField(max_length=100, db_collation='French_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='French_CI_AS')
    name = models.CharField(max_length=255, db_collation='French_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='French_CI_AS')
    session_data = models.TextField(db_collation='French_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


