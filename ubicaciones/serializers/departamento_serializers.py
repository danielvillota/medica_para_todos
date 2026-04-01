from rest_framework import serializers
from ubicaciones.models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields='__all__'