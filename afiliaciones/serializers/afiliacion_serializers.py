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
    fecha_inicio = serializers.DateField(format='%d-%b-%Y')
    fecha_fin = serializers.DateField(format='%d-%b-%Y')
    
    def validate_valor(self, value):
        # Truncar a 2 decimales SIN redondear
        return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    
    def validate(self, attrs):

        if self.instance:
            contrato = attrs.get("contrato", self.instance.contrato)
            provisional = attrs.get("provisional", self.instance.provisional)
            asesor = attrs.get("id_asesor", self.instance.id_asesor)
        else:
            contrato = attrs.get("contrato")
            provisional = attrs.get("provisional")
            asesor = attrs.get("id_asesor")

        # Validar contrato

        contrato_papeleria = Papeleria.objects.filter(
            valor=contrato,
            id_asesor=asesor,
            tipo_documento=1
        ).first()

        if not contrato_papeleria:
            raise serializers.ValidationError({
                "contrato": "El contrato no pertenece al asesor seleccionado."
            })

        if self.instance:
            if contrato != self.instance.contrato and contrato_papeleria.is_asignado:
                raise serializers.ValidationError({
                    "contrato": "El contrato ya se encuentra asignado."
                })
        else:
            if contrato_papeleria.is_asignado:
                raise serializers.ValidationError({
                    "contrato": "El contrato ya se encuentra asignado."
                })

        # Validar provisional

        provisional_papeleria = Papeleria.objects.filter(
            valor=provisional,
            id_asesor=asesor,
            tipo_documento=2
        ).first()

        if not provisional_papeleria:
            raise serializers.ValidationError({
                "provisional": "El provisional no pertenece al asesor seleccionado."
            })

        if self.instance:
            if (
                provisional != self.instance.provisional
                and provisional_papeleria.is_asignado
            ):
                raise serializers.ValidationError({
                    "provisional": "El provisional ya se encuentra asignado."
                })
        else:
            if provisional_papeleria.is_asignado:
                raise serializers.ValidationError({
                    "provisional": "El provisional ya se encuentra asignado."
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
        
    def update(self, instance, validated_data):

        with transaction.atomic():

            # Guardar valores anteriores
            contrato_anterior = instance.contrato
            provisional_anterior = instance.provisional
            asesor_anterior = instance.id_asesor

            # Actualizar la afiliación
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            # CONTRATO

            if (
                contrato_anterior != instance.contrato or
                asesor_anterior != instance.id_asesor
            ):

                # Liberar contrato anterior
                Papeleria.objects.filter(
                    valor=contrato_anterior,
                    id_asesor=asesor_anterior,
                    tipo_documento=1
                ).update(
                    is_asignado=False
                )

                # Asignar nuevo contrato
                Papeleria.objects.filter(
                    valor=instance.contrato,
                    id_asesor=instance.id_asesor,
                    tipo_documento=1
                ).update(
                    is_asignado=True
                )

            # PROVISIONAL

            if (
                provisional_anterior != instance.provisional or
                asesor_anterior != instance.id_asesor
            ):

                # Liberar provisional anterior
                Papeleria.objects.filter(
                    valor=provisional_anterior,
                    id_asesor=asesor_anterior,
                    tipo_documento=2
                ).update(
                    is_asignado=False
                )

                # Asignar nuevo provisional
                Papeleria.objects.filter(
                    valor=instance.provisional,
                    id_asesor=instance.id_asesor,
                    tipo_documento=2
                ).update(
                    is_asignado=True
                )

        return instance
    
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

class AfiliacionReporteSerializer(serializers.ModelSerializer):
    nombre_titular=serializers.CharField(source='id_titular.nombre')
    nombre_asesor=serializers.CharField(source='id_asesor.nombre')
    celular=serializers.CharField(source='id_titular.celular')
    municipio=serializers.CharField(source='id_titular.id_municipio.nombre')
    direccion=serializers.CharField(source='id_titular.direccion')
    fecha_fin = serializers.DateField(format='%d-%b-%Y', read_only=True)
    saldo=serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model=Afiliacion
        fields=['nombre_titular','celular','nombre_asesor','municipio','direccion','fecha_fin','saldo']