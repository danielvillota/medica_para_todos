from rest_framework import serializers
from beneficiarios.models import Beneficiario

class BeneficiarioSerializer(serializers.ModelSerializer):
    usuario_correo=serializers.EmailField(source='usuario.email', read_only=True)
    class Meta:
        model = Beneficiario
        fields = '__all__'