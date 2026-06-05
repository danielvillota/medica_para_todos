from django.db import models
from bodega.enum.enum_documento import DocumentoChoices

class Papeleria(models.Model):
    tipo_documento=models.IntegerField(choices=DocumentoChoices.choices)
    valor=models.CharField(max_length=6, unique=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    is_asignado=models.BooleanField(default=False)
    id_usuario=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='papelerias_creada', db_index=True)
    id_usuario_updated=models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='papelerias_actualizada', db_index=True)
    id_asesor=models.ForeignKey('asesores.Asesor', on_delete=models.PROTECT, related_name='papelerias', db_index=True)
    
    