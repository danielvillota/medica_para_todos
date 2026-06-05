from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bodega.models import Papeleria
from bodega.serializers import PapeleriaSerializer

class PapeleriaView(APIView):
    def get(self, request):
        papelerias=Papeleria.objects.all()
        serializer=PapeleriaSerializer(papelerias, many=True)
        return Response({
            "message":"Lista de papeleria registrada",
            "data":serializer.data
        },status=status.HTTP_200_OK)  
    
    def post(self, request):
        serializer=PapeleriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Papeleria registrada exitosamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "errors":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
        
class PapeleriaDetalleView(APIView):
    def patch(self, request, id):
        try:
            papeleria=Papeleria.objects.get(id=id)
        except Papeleria.DoesNotExist:
            return Response({
                "message":"No existe la papeleria"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=PapeleriaSerializer(papeleria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Papeleria actualizada exitosamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"Error de validaciones",
            "errors":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            papeleria=Papeleria.objects.get(id=id)
        except Papeleria.DoesNotExist:
            return Response({
                "message":"no existe la papeleria"
            },status=status.HTTP_404_NOT_FOUND)
        if papeleria.is_asignado==False:
            papeleria.delete()
            return Response({
                "message":"El tipo de documento fue eliminado exitosamente"
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "message":"el tipo de documento esta asignado a una afiliacion"
            },status=status.HTTP_200_OK)