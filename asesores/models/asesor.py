from django.db import models

class Asesor(models.Model):
    nombre=models.CharField(max_length=100)
    codigo=models.CharField(max_length=4, unique=True)
    cedula=models.CharField(unique=True, max_length=15)
    direccion=models.CharField(max_length=50, null=True)
    celular=models.CharField(max_length=10, null=True)
    is_active=models.BooleanField(default=True, db_index=True)
