from rest_framework import serializers
from especialistas.models import Especialista, Orden

class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Especialista
        fields='__all__'

class EspecialistaOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orden
        fields='__all__'