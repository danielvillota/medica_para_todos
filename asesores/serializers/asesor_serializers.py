from rest_framework import serializers
from asesores.models import Asesor

class AsesorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asesor
        fields='__all__'