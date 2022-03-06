from django.db import models

class Usuario(models.Model):
    nombre=models.CharField(max_length=255)
    apellido=models.CharField(max_length=255)
    correo=models.CharField(max_length=255)
    telefono=models.CharField(max_length=10)

