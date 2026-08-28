from django.db import models
from especialistas.enums.enum_orden import OrdenChoices, OrdenEstadoChoices

class Orden(models.Model):
    fecha_registro=models.DateField(null=True)
    contrato=models.CharField(max_length=6)
    afiliado=models.CharField(max_length=100)
    identificacion=models.CharField(max_length=25, null=True)
    celular=models.CharField(max_length=25, null=True)
    municipio=models.CharField(max_length=50, null=True)
    nombre_especialista=models.CharField(max_length=150, null=True)
    especialidad=models.CharField(max_length=150)
    estado_cita=models.IntegerField(choices=OrdenChoices.choices, default=OrdenChoices.CONSULTA)
    fecha_cita=models.DateField(null=True)
    hora=models.CharField(max_length=10, null=True)
    direccion=models.CharField(max_length=250, null=True)
    observacion_cita=models.CharField(max_length=300, null=True)
    particular=models.IntegerField(null=True)
    descuento=models.IntegerField()
    estado=models.IntegerField(choices=OrdenEstadoChoices.choices, default=OrdenEstadoChoices.PENDIENTE)
    observacion=models.CharField(max_length=200, null=True)
    secretaria=models.CharField(max_length=100)
    id_usuario=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='ordenes_creada', db_index=True)
    id_usuario_updated=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='ordenes_actualizada', db_index=True)
    