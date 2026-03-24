from django.db import models

class RoleChoices(models.IntegerChoices):
    ADMINISTRADOR = 1, 'Administrador'
    DIGITACION = 2, 'Digitador'