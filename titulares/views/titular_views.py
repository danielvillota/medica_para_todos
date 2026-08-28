from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from titulares.serializers import TitularSerializer
from titulares.models import Titular

class TitularView(APIView):
    def post(self, request):
        serializer=TitularSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Titular creado exitosamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        titulares=Titular.objects.all()
        serializer=TitularSerializer(titulares, many=True)
        return Response({
            "message":"Lista de titulares",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
class TitularDetalleView(APIView):
    def get(self, request, id):
        try:
            titular=Titular.objects.get(id=id)
        except Titular.DoesNotExist:
                return Response({
                    "message":"No existe el titular"
                },status=status.HTTP_404_NOT_FOUND)
        serializer=TitularSerializer(titular)
        return Response({
             "message":"Detalle del titular",
             "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        try:
            titular=Titular.objects.get(id=id)
        except Titular.DoesNotExist:
            return Response({
                "message":"No existe el titular"
            },status=status.HTTP_400_BAD_REQUEST)
        serializer=TitularSerializer(titular, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Titular actualizado correctamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)