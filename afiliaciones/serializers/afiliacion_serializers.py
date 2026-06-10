from rest_framework import serializers
from afiliaciones.models import Afiliacion
from decimal import Decimal, ROUND_DOWN

class AfiliacionSerializer(serializers.ModelSerializer):
    nombre_titular=serializers.CharField(source='id_titular.nombre', read_only=True)
    cedula_titular=serializers.CharField(source='id_titular.cedula', read_only=True)
    direccion_titular=serializers.CharField(source='id_titular.direccion', read_only=True)
    municipio_titular=serializers.CharField(source='id_titular.id_municipio.nombre', read_only=True)
    def validate_valor(self, value):
        # Truncar a 2 decimales SIN redondear
        return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    class Meta:
        model=Afiliacion
        fields='__all__'