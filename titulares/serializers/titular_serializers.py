from rest_framework import serializers
from titulares.models import Titular

class TitularSerializer(serializers.ModelSerializer):
    nombre_municipio=serializers.CharField(source='id_municipio.nombre', read_only=True)
    id_departamento = serializers.IntegerField(source='id_municipio.id_departamento_id',read_only=True)
    class Meta:
        model=Titular
        fields='__all__'