from rest_framework import serializers
from afiliaciones.models import Afiliacion
from decimal import Decimal, ROUND_DOWN

class AfiliacionSerializer(serializers.ModelSerializer):
    def validate_valor(self, value):
        # Truncar a 2 decimales SIN redondear
        return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    class Meta:
        model=Afiliacion
        fields='__all__'