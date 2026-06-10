from rest_framework import serializers
from beneficiarios.models import Beneficiario

class BeneficiarioSerializer(serializers.ModelSerializer):
    usuario_correo=serializers.EmailField(source='id_usuario.email', read_only=True)
    titular=serializers.CharField(source='id_titular.nombre')
    cedula=serializers.CharField(source='id_titular.cedula')
    class Meta:
        model = Beneficiario
        fields = '__all__'