from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bodega.models import Papeleria
from bodega.serializers import PapeleriaSerializer
from paginacion.paginacion import Paginacion
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class PapeleriaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        papelerias=Papeleria.objects.all()
        paginador=Paginacion()
        pagina = paginador.paginate_queryset(
            papelerias,
            request
        )
        serializer=PapeleriaSerializer(pagina, many=True)
        return paginador.get_paginated_response(
            serializer.data
        )
    
    def post(self, request):
        serializer=PapeleriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_usuario=request.user, id_usuario_updated=request.user)
            return Response({
                "message":"Papeleria registrada exitosamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "errors":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
        
class PapeleriaDetalleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, id):
        try:
            papeleria=Papeleria.objects.get(id=id)
        except Papeleria.DoesNotExist:
            return Response({
                "message":"No existe la papeleria"
            },status=status.HTTP_404_NOT_FOUND)
        
        if papeleria.is_asignado:
            return Response({
                "message": "No se puede modificar una papelería asignada"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        serializer=PapeleriaSerializer(papeleria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(id_usuario_updated=request.user)
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
            },status=status.HTTP_400_BAD_REQUEST)