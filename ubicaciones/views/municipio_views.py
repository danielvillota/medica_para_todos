from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ubicaciones.models.municipio import Municipio
from ubicaciones.serializers import MunicipioSerializer

class MunicipioView(APIView):
    def get(self, request, id_departamento):
        try:
            municipios=Municipio.objects.filter(id_departamento=id_departamento)
            serializer=MunicipioSerializer(municipios, many=True)
            return Response({
                "message":"Lista de municipios segun el departamento",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":"Error al obtener municipios",
                "error":str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)