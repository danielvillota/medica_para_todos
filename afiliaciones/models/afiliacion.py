from django.db import models

class Afiliacion(models.Model):
    contrato=models.CharField(max_length=6, unique=True)
    provisional=models.CharField(max_length=6, unique=True)
    valor=models.DecimalField(max_digits=15, decimal_places=2)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    is_active=models.BooleanField(default=True, db_index=True)
    id_titular=models.ForeignKey('titulares.titular', on_delete=models.PROTECT, related_name='afiliaciones', db_index=True)