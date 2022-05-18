# Generated by Django 4.0.4 on 2022-05-18 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPersonnel', '0005_gradeechellon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statutgrade',
            fields=[
                ('idstatutgrade', models.AutoField(db_column='idStatutGrade', primary_key=True, serialize=False)),
                ('statutgradefr', models.CharField(blank=True, db_collation='French_CI_AS', db_column='StatutGradeFr', max_length=30, null=True)),
                ('statutgradear', models.CharField(blank=True, db_collation='French_CI_AS', db_column='StatutGradeAr', max_length=30, null=True)),
            ],
            options={
                'db_table': 'StatutGrade',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Gradeechellon',
        ),
        migrations.DeleteModel(
            name='Indice',
        ),
    ]
