from django.db import models

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
    photo = models.ImageField(upload_to="")
    age = models.IntegerField(db_column='Age', blank=True, null=True)
    lastupdate = models.DateField(db_column='LastUpdate', blank=True, null=True)
    ppr = models.CharField(db_column='Ppr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    organisme = models.CharField(db_column='Organisme', max_length=80, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Personnel'
        verbose_name = "الموظف"
        verbose_name_plural = "الموظفين"

# -------------------------------------------------------
class Fonction(models.Model):
    idfonction = models.AutoField(db_column='IdFonction', primary_key=True)
    libellefontionar = models.CharField(db_column='LibelleFontionAr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)
    libellefonctionfr = models.CharField(db_column='LibelleFonctionFr', max_length=50, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Fonction'
        verbose_name = "المهمة"
        verbose_name_plural = "المهمات"
# -------------------------------------------------------
class Fonctionpersonnel(models.Model):
    idfonctionpersonnel = models.AutoField(db_column='IdFonctionPersonnel', primary_key=True)
    idfonction_field = models.ForeignKey('Fonction', models.DO_NOTHING, db_column='IdFonction#')
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')
    datefonction = models.DateTimeField(db_column='DateFonction')

    class Meta:
        managed = False
        db_table = 'FonctionPersonnel'
        unique_together = (('idfonction_field', 'datefonction'),)
        verbose_name = "مهمة الموظف"
        verbose_name_plural = "مهمة الموظفين"

# -------------------------------------------------------
class Concours(models.Model):
    idconcours = models.AutoField(db_column='IdConcours', primary_key=True)
    libelleconcoursar = models.CharField(db_column='LibelleConcoursAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    libelleconcoursfr = models.CharField(db_column='LibelleConcoursFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    dateconcours = models.DateTimeField(db_column='DateConcours', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Concours'
        verbose_name = "الإمتحان"
        verbose_name_plural = "الإمتحانات"


# -------------------------------------------------------
class Echelle(models.Model):
    idechelle = models.AutoField(db_column='IdEchelle', primary_key=True)
    echelle = models.IntegerField(db_column='Echelle', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Echelle'
        verbose_name = "السلم"
        verbose_name_plural = "السلم"
    def __str__(self):
        return self.echelle


# -------------------------------------------------------
class Echellon(models.Model):
    idechellon = models.AutoField(db_column='IdEchellon', primary_key=True)
    echellon = models.CharField(db_column='Echellon', max_length=30, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Echellon'
        verbose_name = "الرتبة"
        verbose_name_plural = "الرتب"

# -------------------------------------------------------
class Statutgrade(models.Model):
    idstatutgrade = models.AutoField(db_column='idStatutGrade', primary_key=True)
    statutgradefr = models.CharField(db_column='StatutGradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    statutgradear = models.CharField(db_column='StatutGradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'StatutGrade'
        verbose_name = "حالة الدرجة"
        verbose_name_plural = "حالة الدرجات"
    def __str__(self):
        return self.statutgradear


# -------------------------------------------------------
class Grade(models.Model):
    idgrade = models.AutoField(db_column='IdGrade', primary_key=True)
    gradear = models.CharField(db_column='GradeAr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    gradefr = models.CharField(db_column='GradeFr', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    idstatutgrade_field = models.ForeignKey('Statutgrade', models.DO_NOTHING, db_column='idStatutGrade#', blank=True, null=True)
    idechelle_field = models.ForeignKey(Echelle, models.DO_NOTHING, db_column='idEchelle#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Grade'
        verbose_name = "الدرجة"
        verbose_name_plural = "الدرجات"

# -------------------------------------------------------
class Gradepersonnel(models.Model):
    idgradepersonnel = models.AutoField(db_column='IdGradePersonnel', primary_key=True)
    idgrade_field = models.ForeignKey(Grade, models.DO_NOTHING, db_column='IdGrade#', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    dategrade = models.DateTimeField(db_column='DateGrade', blank=True, null=True)
    changementdegrade = models.CharField(db_column='ChangementDeGrade', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    idechellon_field = models.ForeignKey(Echellon, models.DO_NOTHING, db_column='idEchellon#', blank=True,null=True)
    indice = models.CharField(db_column='Indice', max_length=15, db_collation='French_CI_AS', blank=True,null=True)
    dateechellon = models.DateTimeField(db_column='DateEchellon', blank=True, null=True)
    changementdechellon = models.CharField(db_column='ChangementDEchellon', max_length=100, db_collation='French_CI_AS',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GradePersonnel'
        unique_together = (('idgrade_field', 'idpersonnel_field','idechellon_field'),)
        verbose_name = "درجة الموظف"
        verbose_name_plural = "درجة الموظفين"

# -------------------------------------------------------
class Conjoint(models.Model):
    idconjoint = models.AutoField(db_column='IdConjoint', primary_key=True)
    cin = models.CharField(db_column='Cin', max_length=20, db_collation='French_CI_AS', unique=True)
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)
    lieunaissance = models.CharField(db_column='LieuNaissance', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    fonction = models.CharField(db_column='Fonction', max_length=60, db_collation='French_CI_AS', blank=True,null=True)
    ppr = models.CharField(db_column='Ppr', max_length=60, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Conjoint'
        verbose_name = "الزوج"
        verbose_name_plural = "الأزواج"
# -------------------------------------------------------
class Conjointpersonnel(models.Model):
    idconjoint_field = models.OneToOneField(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', primary_key=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#')

    class Meta:
        managed = False
        db_table = 'ConjointPersonnel'
        unique_together = (('idconjoint_field', 'idpersonnel_field'),)
        verbose_name = "زوج الموظف"
        verbose_name_plural = "زوج الموظفين"
# -------------------------------------------------------
class Enfant(models.Model):
    idenfant = models.AutoField(db_column='IdEnfant', primary_key=True)
    nomar = models.CharField(db_column='NomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    nomfr = models.CharField(db_column='NomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomar = models.CharField(db_column='PrenomAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    prenomfr = models.CharField(db_column='PrenomFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    datenaissance = models.DateTimeField(db_column='DateNaissance', blank=True, null=True)
    lieunaissancear = models.CharField(db_column='LieuNaissanceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    lieunaissancefr = models.CharField(db_column='LieuNaissanceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    lienjuridique = models.CharField(db_column='LienJuridique', max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    idconjoint_field = models.ForeignKey(Conjoint, models.DO_NOTHING, db_column='IdConjoint#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Enfant'
        verbose_name = "الطفل"
        verbose_name_plural = "الأطفال"

# -------------------------------------------------------
class Entite(models.Model):
    identite = models.AutoField(db_column='IdEntite', primary_key=True)
    libelleentitenar = models.CharField(db_column='LibelleEntitenAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    libelleentitefr = models.CharField(db_column='LibelleEntiteFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Entite'
        verbose_name = "الهيئة"
        verbose_name_plural = "الهيئات"
# -------------------------------------------------------
class District(models.Model):
    iddistrict = models.AutoField(db_column='IdDistrict', primary_key=True)
    libelledistrictar = models.CharField(db_column='LibelleDistrictAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    libelledistrictfr = models.CharField(db_column='LibelleDistrictFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    identite_field = models.ForeignKey('Entite', models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'District'
        verbose_name = "المنطقة"
        verbose_name_plural = "المنطقات"

# -------------------------------------------------------
class Annexe(models.Model):
    idannexe = models.AutoField(db_column='IdAnnexe', primary_key=True)
    libelleannexear = models.CharField(db_column='LibelleAnnexeAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    libelleannexefr = models.CharField(db_column='LibelleAnnexeFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    iddistrict_field = models.ForeignKey('District', models.DO_NOTHING, db_column='IdDistrict#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Annexe'
        verbose_name = "الملحقة"
        verbose_name_plural = "الملحقات"

# -------------------------------------------------------
class Annexepersonnel(models.Model):
    idannexepersonnel = models.AutoField(db_column='IdAnnexePersonnel', primary_key=True)
    idannexe_field = models.ForeignKey(Annexe, models.DO_NOTHING, db_column='IdAnnexe#', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AnnexePersonnel'
        verbose_name = "ملحقة الموظف"
        verbose_name_plural = "ملحقة الموظفين"

# -------------------------------------------------------
class Caidat(models.Model):
    idcaidat = models.AutoField(db_column='IdCaidat', primary_key=True)
    libellecaidatar = models.CharField(db_column='LibelleCaidatAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    libellecaidatfr = models.CharField(db_column='LibelleCaidatFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    idcercle_field = models.ForeignKey('Cercle', models.DO_NOTHING, db_column='IdCercle#', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Caidat'
        verbose_name = "القيادة"
        verbose_name_plural = "القيادات"



class Caidatpersonnel(models.Model):
    idcaidatpersonnel = models.AutoField(db_column='IdCaidatPersonnel', primary_key=True)
    idcaidat_field = models.ForeignKey(Caidat, models.DO_NOTHING, db_column='IdCaidat#', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'CaidatPersonnel'
        verbose_name = "قيادة الموظف"
        verbose_name_plural = "قيادة الموظفين"


class Cercle(models.Model):
    idcercle = models.AutoField(db_column='IdCercle', primary_key=True)
    libellecerclear = models.CharField(db_column='LibelleCercleAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    libellecerclefr = models.CharField(db_column='LibelleCercleFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    identite_field = models.ForeignKey('Entite', models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Cercle'
        verbose_name = "الدائرة"
        verbose_name_plural = "الدائرات"

# -------------------------------------------------------

class Division(models.Model):
    iddivision = models.AutoField(db_column='IdDivision', primary_key=True)
    libelledivisionar = models.CharField(db_column='LibelleDivisionAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    libelledivisionfr = models.CharField(db_column='LibelleDivisionFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    identite_field = models.ForeignKey('Entite', models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Division'
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"

# -------------------------------------------------------
class Service(models.Model):
    idservice = models.AutoField(db_column='IdService', primary_key=True)
    libelleservicear = models.CharField(db_column='LibelleServiceAr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    libelleservicefr = models.CharField(db_column='LibelleServiceFr', max_length=20, db_collation='French_CI_AS', blank=True, null=True)
    iddivision_field = models.ForeignKey(Division, models.DO_NOTHING, db_column='IdDivision#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Service'
        verbose_name = "المصلحة"
        verbose_name_plural = "المصلحات"
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
        verbose_name = "مصلحة الموظف"
        verbose_name_plural = "مصلحة الموظفين"

# -------------------------------------------------------
class Pashalik(models.Model):
    idpashalik = models.AutoField(db_column='IdPashalik', primary_key=True)
    libellepashalikar = models.CharField(db_column='LibellePashalikAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    libellepashalikfr = models.CharField(db_column='LibellePashalikFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)
    identite_field = models.ForeignKey(Entite, models.DO_NOTHING, db_column='IdEntite#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pashalik'
        verbose_name = "الباشوية"
        verbose_name_plural = "الباشاويات"

# -------------------------------------------------------
class Reafectation(models.Model):
    idreafectation = models.AutoField(db_column='IdReafectation', primary_key=True)
    libellereafectationar = models.CharField(db_column='LibelleReafectationAr', max_length=80, db_collation='French_CI_AS', blank=True, null=True)
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#')
    libellereafectationfr = models.CharField(db_column='LibelleReafectationFr', max_length=80, db_collation='French_CI_AS', blank=True, null=True)
    idorganismeparent = models.IntegerField(db_column='IdOrganismeParent', blank=True, null=True)
    organisme = models.CharField(db_column='Organisme', max_length=80, db_collation='French_CI_AS', blank=True, null=True)
    datereafectation = models.DateTimeField(db_column='DateReafectation', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reafectation'
        verbose_name = "التعيين"
        verbose_name_plural = "التعيينات"

# -------------------------------------------------------
class Pashalikpersonnel(models.Model):
    idpashalikpersonnel = models.AutoField(db_column='IdPashalikPersonnel', primary_key=True)
    idpashalik_field = models.ForeignKey(Pashalik, models.DO_NOTHING, db_column='IdPashalik#', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    dateaffectation = models.DateTimeField(db_column='DateAffectation', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PashalikPersonnel'
        verbose_name = "باشوية الموظف"
        verbose_name_plural = "باشوية الموظفين"

# -------------------------------------------------------
class Diplome(models.Model):
    iddiplome = models.AutoField(db_column='IdDiplome', primary_key=True)
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
        verbose_name = "الشهادة"
        verbose_name_plural = "الشهادات"

# -------------------------------------------------------
class ParametrageRetraite(models.Model):
    idparametrageretraite = models.AutoField(db_column='IdParametrageRetraite', primary_key=True)
    nbannee = models.IntegerField(db_column='NbAnnee', blank=True, null=True)
    nbmois = models.IntegerField(db_column='NbMois', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ParametrageRetraite'
        verbose_name = "عدد سنوات التقاعد"
        verbose_name_plural = "عدد سنوات التقاعد"

 # -------------------------------------------------------
class Statut(models.Model):
    idstatut = models.AutoField(db_column='IdStatut', primary_key=True)  # Field name made lowercase.
    libellestatutar = models.CharField(db_column='LibelleStatutAr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.
    libellestatutfr = models.CharField(db_column='LibelleStatutFr', max_length=100, db_collation='French_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Statut'
        verbose_name = "الحالة النضامية"
        verbose_name_plural = "الحالات النضامية"


class Statutpersonnel(models.Model):
    idstatutpersonnel = models.AutoField(db_column='IdStatutPersonnel', primary_key=True)  # Field name made lowercase.
    idstatut_field = models.ForeignKey(Statut, models.DO_NOTHING, db_column='IdStatut#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    idpersonnel_field = models.ForeignKey(Personnel, models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    datestatut = models.DateTimeField(db_column='DateStatut', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StatutPersonnel'
        verbose_name = "حالة الموظف"
        verbose_name_plural = "حالة الموظفين"


class Attestationtravail(models.Model):
    idattestationtravail = models.AutoField(db_column='IdAttestationTravail', primary_key=True)
    numattestationtravail = models.IntegerField(db_column='NumAttestationTravail', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    datedelivre = models.DateTimeField(db_column='DateDelivre', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AttestationTravail'
        verbose_name = "شهادة العمل"
        verbose_name_plural = "شهادات العمل"


class QuitterTerritoire(models.Model):
    idquitterterritoire = models.AutoField(db_column='IdQuitterTerritoire', primary_key=True)
    numquitterterritoire = models.IntegerField(db_column='NumQuitterTerritoire', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)
    datedelivre = models.DateTimeField(db_column='DateDelivre', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'QuitterTerritoire'
        verbose_name = "شهادة مغادرة التراب الوطني"
        verbose_name_plural = "شهادات مغادرة التراب الوطني"
