# Generated by Django 4.0.2 on 2022-03-28 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('agrupaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contratacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.CharField(max_length=255)),
                ('tiempo', models.IntegerField()),
                ('direccion', models.CharField(max_length=255)),
                ('calificacion', models.CharField(max_length=255, null=True)),
                ('rating', models.IntegerField(null=True)),
                ('estado', models.CharField(max_length=255)),
                ('agrupacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agrupaciones.agrupacion')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Facturacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abono', models.IntegerField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('contratacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contrataciones.contratacion')),
            ],
        ),
    ]
