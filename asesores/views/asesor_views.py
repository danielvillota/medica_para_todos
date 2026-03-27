from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asesores.models import Asesor
from asesores.serializers import AsesorSerializer

class AsesorView(APIView):
    def post(self, request):
        serializer=AsesorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Asesor creado exitosamente",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message":"error validaciones",
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            asesores=Asesor.objects.filter(is_active=True)
            serializer=AsesorSerializer(asesores, many=True)
            return Response({
                "message":"Lista de asesores",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message":"Eror al obtener asesores",
                "error":str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AsesorDetalleView(APIView):
    def get(self, request, id):
        try:
            asesor=Asesor.objects.get(id=id)
        except Asesor.DoesNotExist:
            return Response({
                "message":"No existe el asesor"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer=AsesorSerializer(asesor)
    
        return Response({
            "message":"Detalle asesor",
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        try:
            asesor=Asesor.objects.get(id=id)
        except Asesor.DoesNotExist:
            return Response({
                "message":"Asesor no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=AsesorSerializer(asesor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mesage":"Asesor modificado exitosamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            asesor=Asesor.objects.get(id=id)
        except Asesor.DoesNotExist:
            return Response({
                "message":"Asesor no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        asesor.is_active=False
        asesor.save()
        return Response({
            "message":"Asesor desactivado exitosamente"
        },status=status.HTTP_200_OK)
