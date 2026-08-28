from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ubicaciones.models.departamento import Departamento
from ubicaciones.serializers import DepartamentoSerializer

class DepartamentoView(APIView):
    def get(self, request):
        departamentos=Departamento.objects.all()
        serializer=DepartamentoSerializer(departamentos, many=True)
        
        return Response({
            "message":"Lista de departamentos",
            "data":serializer.data
        },status=status.HTTP_200_OK)
