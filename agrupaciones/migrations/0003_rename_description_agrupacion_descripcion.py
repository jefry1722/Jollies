# Generated by Django 4.0.2 on 2022-03-13 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agrupaciones', '0002_agrupacion_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agrupacion',
            old_name='description',
            new_name='descripcion',
        ),
    ]
