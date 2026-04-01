from rest_framework import serializers
from ubicaciones.models import Municipio

class MunicipioSerializer(serializers.ModelSerializer):
    departamento_nombre=serializers.CharField(source='departamento.nombre', read_only=True)
    class Meta:
        model = Municipio
        fields = '__all__'