from django.db import models

# Create your models here.
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