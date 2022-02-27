# Generated by Django 4.0.2 on 2022-02-21 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('correo', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Agrupacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=10)),
                ('integrantes', models.IntegerField()),
                ('genero', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agrupaciones.genero')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agrupaciones.manager')),
            ],
        ),
    ]
