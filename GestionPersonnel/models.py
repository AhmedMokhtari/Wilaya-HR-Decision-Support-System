from django.db import models

# Create your models here.

# -------------------------------------------------------
class Personnel(models.Model):
    idpersonnel = models.AutoField(db_column='IdPersonnel', primary_key=True)
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', unique=True)
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)
    lieunaissancear = models.CharField(db_column='LieuNaissanceAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    lieunaissancefr = models.CharField(db_column='LieuNaissanceFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    adressear = models.CharField(db_column='AdresseAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    adressefr = models.CharField(db_column='AdresseFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=40, db_collation='French_CI_AS', blank=True, null=True)
    tele = models.IntegerField(db_column='Tele', blank=True, null=True)
    situationfamilialear = models.CharField(db_column='SituationFamilialeAr', max_length=80, db_collation='French_CI_AS', blank=True, null=True)
    situationfamilialefr = models.CharField(db_column='SituationFamilialeFr', max_length=80, db_collation='French_CI_AS', blank=True, null=True)
    sexe = models.CharField(db_column='Sexe', max_length=90, db_collation='French_CI_AS', blank=True, null=True)
    vaccination = models.BooleanField(db_column='Vaccination', blank=True, null=True)  # Field name made lowercase.
    numerolocation = models.CharField(db_column='NumeroLocation', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    numerofinancier = models.CharField(db_column='NumeroFinancier', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    daterecrutement = models.DateTimeField(db_column='DateRecrutement', blank=True, null=True)
    datedemarcation = models.DateTimeField(db_column='DateDemarcation', blank=True, null=True)
    dateparrainageretraite = models.DateTimeField(db_column='DateParrainageRetraite', blank=True, null=True)
    cmr = models.CharField(db_column='Cmr', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    posteemploye = models.CharField(db_column='PosteEmploye', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    metier = models.CharField(db_column='Metier', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    typeemploye = models.CharField(db_column='TypeEmploye', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    tachesprecedentes = models.CharField(db_column='TachesPrecedentes', max_length=60, db_collation='French_CI_AS', blank=True, null=True)
    rib = models.IntegerField(db_column='Rib', blank=True, null=True)  # Field name made lowercase.
    ancienneteadmi = models.CharField(db_column='ancienneteAdmi', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    numcnopsaf = models.CharField(db_column='NumCnopsAf', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    numcnopsim = models.CharField(db_column='NumCnopsIm', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    administrationapp = models.CharField(db_column='AdministrationApp', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    photo = models.ImageField(upload_to="photos")
    age = models.IntegerField(db_column='Age', blank=True, null=True)
    lastupdate = models.DateField(db_column='LastUpdate', blank=True, null=True)
    statut = models.CharField(db_column='Statut', max_length=40, db_collation='French_CI_AS', blank=True, null=True)
    ppr = models.CharField(db_column='Ppr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    #annexe = models.CharField(db_column='Annexe', max_length=40, db_collation='French_CI_AS', blank=True, null=True)

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
    idfonctionpersonnel = models.AutoField(db_column='IdFonctionPersonnel', primary_key=True)
    idfonction_field = models.ForeignKey('Fonction', models.DO_NOTHING, db_column='IdFonction#')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
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
    idechelle = models.AutoField(db_column='IdEchelle', primary_key=True)
    echelle = models.IntegerField(db_column='Echelle', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Echelle'


# -------------------------------------------------------
class Echellon(models.Model):
    idechellon = models.AutoField(db_column='IdEchellon', primary_key=True)
    echellon = models.CharField(db_column='Echellon', max_length=30, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Echellon'


# -------------------------------------------------------
class Statutgrade(models.Model):
    idstatutgrade = models.AutoField(db_column='idStatutGrade', primary_key=True)  # Field name made lowercase.
    statutgradefr = models.CharField(db_column='StatutGradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    statutgradear = models.CharField(db_column='StatutGradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StatutGrade'

# -------------------------------------------------------
class Grade(models.Model):
    idgrade = models.AutoField(db_column='IdGrade', primary_key=True)  # Field name made lowercase.
    gradear = models.CharField(db_column='GradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    gradefr = models.CharField(db_column='GradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idstatutgrade_field = models.ForeignKey('Statutgrade', models.DO_NOTHING, db_column='idStatutGrade#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='idEchelle#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Grade'

# -------------------------------------------------------
class Gradepersonnel(models.Model):
    idgradepersonnel = models.AutoField(db_column='IdGradePersonnel', primary_key=True)  # Field name made lowercase.
    idgrade_field = models.ForeignKey(Grade, models.DO_NOTHING, db_column='IdGrade#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)  # Field name made lowercase.
    changementdegrade = models.CharField(db_column='ChangementDeGrade', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    idechellon_field = models.ForeignKey(Echellon, models.DO_NOTHING, db_column='idEchellon#', blank=True,null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    indice = models.CharField(db_column='Indice', max_length=15, db_collation='French_CI_AS', blank=True,null=True)  # Field name made lowercase.
    dateechellon = models.DateTimeField(db_column='DateEchellon', blank=True, null=True)  # Field name made lowercase.
    changementdechellon = models.CharField(db_column='ChangementDEchellon', max_length=100, db_collation='French_CI_AS',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GradePersonnel'
        unique_together = (('idgrade_field', 'idpersonnel_field','idechellon_field'),)

# -------------------------------------------------------
class Conjoint(models.Model):
    idconjoint = models.AutoField(db_column='IdConjoint', primary_key=True)
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', unique=True)
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)  # Field name made lowercase.
    lieunaissance = models.CharField(db_column='LieuNaissance', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    fonction = models.CharField(db_column='Fonction', max_length=60, db_collation='French_CI_AS', blank=True,null=True)
    ppr = models.CharField(db_column='Ppr', max_length=60, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Conjoint'
# -------------------------------------------------------
class Conjointpersonnel(models.Model):
    idconjoint_field = models.OneToOneField(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', primary_key=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')

    class Meta:
        managed = False
        db_table = 'ConjointPersonnel'
        unique_together = (('idconjoint_field', 'idpersonnel_field'),)

# -------------------------------------------------------
class Enfant(models.Model):
    idenfant = models.AutoField(db_column='IdEnfant', primary_key=True)  # Field name made lowercase.
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)  # Field name made lowercase.
    lieunaissancear = models.CharField(db_column='LieuNaissanceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    lieunaissancefr = models.CharField(db_column='LieuNaissanceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    lienjuridique = models.CharField(db_column='LienJuridique', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    idconjoint_field = models.ForeignKey(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Enfant'

# -------------------------------------------------------
class Entite(models.Model):
    identite = models.AutoField(db_column='IdEntite', primary_key=True)  # Field name made lowercase.
    libelleentitenar = models.CharField(db_column='LibelleEntitenAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleentitefr = models.CharField(db_column='LibelleEntiteFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Entite'
# -------------------------------------------------------
class District(models.Model):
    iddistrict = models.AutoField(db_column='IdDistrict', primary_key=True)  # Field name made lowercase.
    libelledistrictar = models.CharField(db_column='LibelleDistrictAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelledistrictfr = models.CharField(db_column='LibelleDistrictFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    identite_field = models.ForeignKey('Entite', models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'District'

# -------------------------------------------------------
class Annexe(models.Model):
    idannexe = models.AutoField(db_column='IdAnnexe', primary_key=True)  # Field name made lowercase.
    libelleannexear = models.CharField(db_column='LibelleAnnexeAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleannexefr = models.CharField(db_column='LibelleAnnexeFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    iddistrict_field = models.ForeignKey('District', models.DO_NOTHING, db_column='IdDistrict#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Annexe'

# -------------------------------------------------------
class Annexepersonnel(models.Model):
    idannexepersonnel = models.AutoField(db_column='IdAnnexePersonnel', primary_key=True)  # Field name made lowercase.
    idannexe_field = models.ForeignKey(Annexe, models.DO_NOTHING, db_column='IdAnnexe#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AnnexePersonnel'
# -------------------------------------------------------
class Division(models.Model):
    iddivision = models.AutoField(db_column='IdDivision', primary_key=True)  # Field name made lowercase.
    libelledivisionar = models.CharField(db_column='LibelleDivisionAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelledivisionfr = models.CharField(db_column='LibelleDivisionFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    identite_field = models.ForeignKey('Entite', models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Division'



# -------------------------------------------------------
class Service(models.Model):
    idservice = models.AutoField(db_column='IdService', primary_key=True)  # Field name made lowercase.
    libelleservicear = models.CharField(db_column='LibelleServiceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libelleservicefr = models.CharField(db_column='LibelleServiceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    iddivision_field = models.ForeignKey(Division, models.DO_NOTHING, db_column='IdDivision#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Service'
    def __str__(self):
        return self.libelleservicefr


# -------------------------------------------------------
class Servicepersonnel(models.Model):
    idservicepersonnel = models.AutoField(db_column='IdServicePersonnel', primary_key=True)
    idservice_field = models.ForeignKey(Service, models.DO_NOTHING, db_column='IdService#')
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#')
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ServicePersonnel'
        unique_together = (('idservice_field', 'idpersonnel_field'),)

# -------------------------------------------------------
class Pashalik(models.Model):
    idpashalik = models.AutoField(db_column='IdPashalik', primary_key=True)  # Field name made lowercase.
    libellepashalikar = models.CharField(db_column='LibellePashalikAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellepashalikfr = models.CharField(db_column='LibellePashalikFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    identite_field = models.ForeignKey(Entite, models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'Pashalik'

# -------------------------------------------------------
class Pashalikpersonnel(models.Model):
    idpashalikpersonnel = models.AutoField(db_column='IdPashalikPersonnel', primary_key=True)  # Field name made lowercase.
    idpashalik_field = models.ForeignKey(Pashalik, models.DO_NOTHING, db_column='IdPashalik#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PashalikPersonnel'
# -------------------------------------------------------
class Diplome(models.Model):
    iddiplome = models.AutoField(db_column='IdDiplome', primary_key=True)  # Field name made lowercase.
    diplomefr = models.CharField(db_column='DiplomeFr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)
    diplomear = models.CharField(db_column='DiplomeAr', max_length=40, db_collation='French_CI_AS', blank=True, null=True)
    etablissement = models.CharField(db_column='Etablissement', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    specialitear = models.CharField(db_column='SpecialiteAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    specialitefr = models.CharField(db_column='SpecialiteFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    datediplome = models.DateTimeField(db_column='DateDiplome', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')

    class Meta:
        managed = False
        db_table = 'Diplome'

