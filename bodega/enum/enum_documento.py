from django.db import models

class DocumentoChoices(models.IntegerChoices):
    CONTRATO=1, 'Contrato'
    PROVISIONAL=2, 'Provisional'
    RECIBO=3, 'Recibo'
    