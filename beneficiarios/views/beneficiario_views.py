from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from beneficiarios.models import Beneficiario
from beneficiarios.serializers import BeneficiarioSerializer

class BeneficiarioView(APIView):
    def post(self, request):
        serializer=BeneficiarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Beneficiario creado correctamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        beneficiarios=Beneficiario.objects.all()
        serializer=BeneficiarioSerializer(beneficiarios, many=True)
        return Response({
            "message":"Lista de beneficiarios",
            "data":serializer.data
        },status=status.HTTP_200_OK)

class BeneficiarioDetalleView(APIView):
    def get(self, request, id):
        try:
            beneficiario=Beneficiario.objects.get(id=id)
        except Beneficiario.DoesNotExist:
            return Response({
                "message":"No existe el beneficiario"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=BeneficiarioSerializer(beneficiario)
        return Response({
            "message":"Detalle beneficiario",
            "data":serializer.data
        },status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            beneficiario=Beneficiario.objects.get(id=id)
        except Beneficiario.DoesNotExist:
            return Response({
                "message":"No existe el beneficiario"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=BeneficiarioSerializer(beneficiario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Beneficiario actualizado correctamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            beneficiario=Beneficiario.objects.get(id=id)
        except Beneficiario.DoesNotExist:
            return Response({
                "message":"No existe el beneficiario",
            },status=status.HTTP_404_NOT_FOUND)
        beneficiario.delete()
        return Response({
            "message":"Beneficiario eliminado exitosamente"
        },status=status.HTTP_200_OK)

class BeneficiarioTitularView(APIView):
    def get(self, request, titular_id):
        beneficiarios=Beneficiario.objects.filter(id_titular_id=titular_id)
        serializer=BeneficiarioSerializer(beneficiarios, many=True)
        return Response({
            "message":"Lista de beneficiarios por titular",
            "data":serializer.data
        },status=status.HTTP_200_OK)