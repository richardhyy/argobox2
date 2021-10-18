# Generated by Django 3.2.4 on 2021-10-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('platformnumber', models.IntegerField(primary_key=True, serialize=False)),
                ('cyclenumber', models.IntegerField()),
                ('sampledirection', models.CharField(blank=True, max_length=2, null=True)),
                ('datamode', models.CharField(blank=True, max_length=2, null=True)),
                ('julianday', models.CharField(blank=True, max_length=12, null=True)),
                ('datadate', models.CharField(blank=True, max_length=14, null=True)),
                ('qc4date', models.CharField(blank=True, max_length=1, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('qc4location', models.CharField(blank=True, max_length=1, null=True)),
                ('creationdate', models.CharField(blank=True, max_length=14, null=True)),
                ('updatedate', models.CharField(blank=True, max_length=14, null=True)),
                ('geom', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'argoheader',
            },
        ),
    ]
