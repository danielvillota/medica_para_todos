from django.db import models

class Especialista(models.Model):
    nombre_especialista=models.CharField(max_length=150)
    especialidad=models.CharField(max_length=150)
    direccion=models.CharField(max_length=250)
    celular=models.CharField(max_length=50)
    particular=models.IntegerField()
    descuento=models.IntegerField()
    fecha_inicio=models.DateField(null=True)
    fecha_terminacion=models.DateField(null=True)
    estado=models.BooleanField(default=False)
    soporte=models.FileField(
        upload_to="especialistas/",
        null=True,
        blank=True
    )