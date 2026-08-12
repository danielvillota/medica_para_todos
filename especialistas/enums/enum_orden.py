from django.db import models

class OrdenChoices(models.IntegerChoices):
    CONSULTA = 1, 'Consulta'
    EXAMEN = 2, 'Examen'
    CONSULTA_EXAMEN = 3, 'Consulta y examen'

class OrdenEstadoChoices(models.IntegerChoices):
    PENDIENTE = 1, 'Pendiente'
    CONFIRMADO = 2, 'Confirmado'
    CANCELADO = 3, 'Cancelado'