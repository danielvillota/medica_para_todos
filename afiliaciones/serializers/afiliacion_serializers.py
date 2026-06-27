from rest_framework import serializers
from afiliaciones.models import Afiliacion
from decimal import Decimal, ROUND_DOWN
from bodega.models import Papeleria
from django.db import transaction
from beneficiarios.serializers import BeneficiariosListaNombresSerializers

class AfiliacionSerializer(serializers.ModelSerializer):
    nombre_titular=serializers.CharField(source='id_titular.nombre', read_only=True)
    cedula_titular=serializers.CharField(source='id_titular.cedula', read_only=True)
    direccion_titular=serializers.CharField(source='id_titular.direccion', read_only=True)
    municipio_titular=serializers.CharField(source='id_titular.id_municipio.nombre', read_only=True)
    fecha_fin = serializers.DateField(format='%d-%b-%Y', read_only=True)
    fecha_inicio = serializers.DateField(format='%d-%b-%Y', read_only=True)
    
    def validate_valor(self, value):
        # Truncar a 2 decimales SIN redondear
        return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    
    def validate(self, attrs):

        contrato = attrs.get('contrato')
        provisional = attrs.get('provisional')
        asesor = attrs.get('id_asesor')

        existe_contrato = Papeleria.objects.filter(
            valor=contrato,
            id_asesor=asesor,
            tipo_documento=1
        ).first()

        if not existe_contrato:
            raise serializers.ValidationError({
                "contrato":
                "El contrato no pertenece al asesor seleccionado."
            })

        existe_provisional = Papeleria.objects.filter(
            valor=provisional,
            id_asesor=asesor,
            tipo_documento=2
        ).first()

        if not existe_provisional:
            raise serializers.ValidationError({
                "provisional":
                "El provisional no pertenece al asesor seleccionado."
            })

        return attrs
    
    def create(self, validated_data):

        with transaction.atomic():

            afiliacion = Afiliacion.objects.create(**validated_data)

            Papeleria.objects.filter(
                valor=afiliacion.contrato,
                id_asesor=afiliacion.id_asesor,
                tipo_documento=1
            ).update(is_asignado=True)

            Papeleria.objects.filter(
                valor=afiliacion.provisional,
                id_asesor=afiliacion.id_asesor,
                tipo_documento=2
            ).update(is_asignado=True)

            return afiliacion
    
    class Meta:
        model=Afiliacion
        fields='__all__'

class AfiliacionCarnetSerializer(serializers.ModelSerializer):
    fecha_fin = serializers.DateField(format='%d-%b-%Y', read_only=True)
    nombre_titular=serializers.CharField(source='id_titular.nombre', read_only=True)
    codigo_asesor=serializers.CharField(source='id_asesor.codigo', read_only=True)
    beneficiarios = BeneficiariosListaNombresSerializers(source='id_titular.beneficiarios', many=True, read_only=True)
    class Meta:
        model=Afiliacion
        fields=['id','contrato','fecha_fin', 'nombre_titular', 'codigo_asesor', 'beneficiarios']