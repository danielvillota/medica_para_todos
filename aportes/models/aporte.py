from django.db import models

class Aporte(models.Model):
    fecha_recibo=models.DateField()
    abono=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    id_afiliacion=models.ForeignKey('afiliaciones.Afiliacion', on_delete=models.PROTECT, related_name='aportes', db_index=True)
    id_asesor=models.ForeignKey('asesores.Asesor', on_delete=models.PROTECT, related_name='aportes', db_index=True)
    id_usuario=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='aportes', db_index=True)