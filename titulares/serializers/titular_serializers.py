from rest_framework import serializers
from titulares.models import Titular

class TitularSerializer(serializers.ModelSerializer):
    nombre_municipio=serializers.CharField(source='municipio.nombre', read_only=True)
    class Meta:
        model=Titular
        fields='__all__'