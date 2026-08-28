from django.db import models

class Departamento(models.Model):
    id=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=150, db_index=True)