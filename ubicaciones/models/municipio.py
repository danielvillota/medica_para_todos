from django.db import models

class Municipio(models.Model):
    id=models.IntegerField(primary_key=True)
    nombre=models.CharField(max_length=150, db_index=True)
    id_departamento=models.ForeignKey('ubicaciones.departamento', on_delete=models.PROTECT, related_name='municipios', db_index=True)