from rest_framework import serializers
from bodega.models import Papeleria

class PapeleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Papeleria
        fields='__all__'