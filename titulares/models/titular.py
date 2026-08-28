from django.db import models

class Titular(models.Model):
    nombre=models.CharField(max_length=100)
    cedula=models.CharField(max_length=10, unique=True, db_index=True)
    celular=models.CharField(max_length=10, null=True)
    id_municipio=models.ForeignKey('ubicaciones.Municipio', on_delete=models.PROTECT, related_name='titulares', db_index=True)
    direccion=models.CharField(max_length=50, null=True)