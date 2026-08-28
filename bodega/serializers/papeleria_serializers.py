from rest_framework import serializers
from bodega.models import Papeleria

class PapeleriaSerializer(serializers.ModelSerializer):

    class Meta:
        model=Papeleria
        fields='__all__'
    
    def validate(self, attrs):

        tipo_documento = attrs.get('tipo_documento')
        valor = attrs.get('valor')

        consulta = Papeleria.objects.filter(
            tipo_documento=tipo_documento,
            valor=valor
        )

        # Si es actualización, excluir el registro actual
        if self.instance:
            consulta = consulta.exclude(
                id=self.instance.id
            )

        if consulta.exists():
            raise serializers.ValidationError({
                "valor": "Ya existe este documento con ese valor."
            })

        return attrs
    