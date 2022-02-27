from django.db import models


class Manager(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Genero(models.Model):
    nombre = models.CharField(max_length=255)


class Agrupacion(models.Model):
    correo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=10)
    integrantes = models.IntegerField()
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)


class Media(models.Model):
    tipo = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    agrupacion = models.ForeignKey(Agrupacion, on_delete=models.SET_NULL, null=True)
