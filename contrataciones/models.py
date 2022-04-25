from django.db import models

from agrupaciones.models import Agrupacion
from usuarios.models import Usuario


class Contratacion(models.Model):
    fecha = models.DateField()
    hora = models.CharField(max_length=255)
    tiempo = models.IntegerField()
    precio = models.IntegerField(default=0)
    direccion = models.CharField(max_length=255)
    agrupacion = models.ForeignKey(Agrupacion, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    calificacion = models.CharField(max_length=255, null=True)
    rating = models.IntegerField(null=True)
    estado = models.CharField(max_length=255)


class Facturacion(models.Model):
    abono = models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    contratacion = models.ForeignKey(Contratacion, on_delete=models.SET_NULL, null=True)
