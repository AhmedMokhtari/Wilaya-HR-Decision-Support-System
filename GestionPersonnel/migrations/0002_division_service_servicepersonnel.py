# Generated by Django 4.0.4 on 2022-04-20 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPersonnel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('iddivision', models.AutoField(db_column='IdDivision', primary_key=True, serialize=False)),
                ('libelledivisionar', models.CharField(blank=True, db_collation='French_CI_AS', db_column='LibelleDivisionAr', max_length=100, null=True)),
                ('libelledivisionfr', models.CharField(blank=True, db_collation='French_CI_AS', db_column='LibelleDivisionFr', max_length=100, null=True)),
            ],
            options={
                'db_table': 'Division',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('idservice', models.AutoField(db_column='IdService', primary_key=True, serialize=False)),
                ('libelleservicear', models.CharField(blank=True, db_collation='French_CI_AS', db_column='LibelleServiceAr', max_length=20, null=True)),
                ('libelleservicefr', models.CharField(blank=True, db_collation='French_CI_AS', db_column='LibelleServiceFr', max_length=20, null=True)),
            ],
            options={
                'db_table': 'Service',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Servicepersonnel',
            fields=[
                ('idservice_field', models.OneToOneField(db_column='IdService#', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='GestionPersonnel.service')),
                ('dateaffectation', models.DateTimeField(blank=True, db_column='DateAffectation', null=True)),
            ],
            options={
                'db_table': 'ServicePersonnel',
                'managed': False,
            },
        ),
    ]
