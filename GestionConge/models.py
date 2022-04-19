from django.db import models

# Create your models here.
class Conge(models.Model):
    idconge = models.AutoField(db_column='IdConge', primary_key=True)
    type_conge = models.CharField(max_length=30, db_collation='French_CI_AS', blank=True, null=True)
    datedebut = models.DateTimeField(db_column='dateDebut', blank=True, null=True)
    dateretour = models.DateTimeField(db_column='dateRetour', blank=True, null=True)
    nbjour = models.IntegerField(db_column='nbJour', blank=True, null=True)
    idpersonnel_field = models.ForeignKey('GestionPersonnel.Personnel', models.DO_NOTHING, db_column='IdPersonnel#', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Conge'