from rest_framework import serializers
from especialistas.models import Especialista

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Especialista
        fields='__all__'