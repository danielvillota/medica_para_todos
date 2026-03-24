from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UsuarioSerializer
from users.models.usuario import User

class UsuarioView(APIView):
    def post(self, request):
        serializer=UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Usuario creado exitosamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error al crear el usaurio",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        usuarios=User.objects.all()
        serializer=UsuarioSerializer(usuarios, many=True)
        return Response({
            "message":"Lista de usuarios",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class UsuarioDetalleView(APIView):
    def patch(self, request, id):
        try:
            usuario=User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message":"Usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Usuario actualizado",
                "data":serializer.data
            })
        return Response({
            "message":"Error validacion",
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id):
        try:
            usuario=User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message":"usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        
        serializer=UsuarioSerializer(usuario)

        return Response({
            "message":"detalle usuario",
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            usuario = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message":"Usuario no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        
        usuario.is_active=False
        usuario.save()
        return Response({
            "message":"Usuario desactivado correctamente"
        },status=status.HTTP_200_OK)