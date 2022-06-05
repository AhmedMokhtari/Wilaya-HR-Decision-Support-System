# Generated by Django 4.0.4 on 2022-06-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionPersonnel', '0013_delete_attestationtravail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attestationtravail',
            fields=[
                ('idattestationtravail', models.AutoField(db_column='IdAttestationTravail', primary_key=True, serialize=False)),
                ('numattestationtravail', models.IntegerField(blank=True, db_column='NumAttestationTravail', null=True)),
                ('datedelivre', models.DateTimeField(blank=True, db_column='DateDelivre', null=True)),
            ],
            options={
                'db_table': 'AttestationTravail',
                'managed': False,
            },
        ),
    ]
