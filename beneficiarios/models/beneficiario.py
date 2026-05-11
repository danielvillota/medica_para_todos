from django.db import models

class Beneficiario(models.Model):
    nombre=models.CharField(max_length=150)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    id_titular=models.ForeignKey('titulares.Titular', on_delete=models.PROTECT, related_name='beneficiarios', db_index=True)
    id_usuario=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='beneficiarios', db_index=True)