from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from especialistas.models import Especialista
from especialistas.serializers import EspecialistaSerializer
from paginacion.paginacion import Paginacion

class EspecialistaView(APIView):
    def post(self, request):
        serializer=EspecialistaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Especialista creado correctamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        especialistas=Especialista.objects.all()
        paginador=Paginacion()
        pagina = paginador.paginate_queryset(
            especialistas,
            request
        )
        serializer=EspecialistaSerializer(pagina, many=True)
        return paginador.get_paginated_response(
            serializer.data
        )

class EspecialistaDetalleView(APIView):
    def get(self, request, id):
        try:
            especialista=Especialista.objects.get(id=id)
        except Especialista.DoesNotExist:
            return Response({
                "message":"No existe el especialista con ese id"
            },status=status.HTTP_404_NOT_FOUND)
                
        serializer=EspecialistaSerializer(especialista)
        return Response({
            "message":"detalle especialista",
            "data":serializer.data
        },status=status.HTTP_200_OK)
            
    def patch(self, request, id):
        try:
            especialista=Especialista.objects.get(id=id)
        except Especialista.DoesNotExist:
            return Response({
                "message":"No existe el especialista con ese id"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=EspecialistaSerializer(especialista, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"especialista actualizado correctamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            especialista=Especialista.objects.get(id=id)
        except Especialista.DoesNotExist:
            return Response({
                "message":"No existe el especialista con ese id"
            },status=status.HTTP_404_NOT_FOUND)
        especialista.delete()
        return Response({
            "message":"especialista eliminado exitosamente"
        },status=status.HTTP_200_OK)