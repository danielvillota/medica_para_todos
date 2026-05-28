from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from aportes.models import Aporte
from afiliaciones.models import Afiliacion
from aportes.serializers import AporteSerializer
from django.db.models import Sum

class AporteView(APIView):
    def get(self, request, afiliacion_id):
        try:
            afiliacion=Afiliacion.objects.get(id=afiliacion_id)
        except Afiliacion.DoesNotExist:
            return Response({
                "message":"No existe la afiliacion con ese id"
            },status=status.HTTP_404_NOT_FOUND)
        aportes=Aporte.objects.filter(id_afiliacion_id=afiliacion_id)
        serializer=AporteSerializer(aportes, many=True)
        total_abonos=aportes.aggregate(total=Sum('abono'))['total'] or 0
        saldo_actual = afiliacion.valor - total_abonos
        return Response({
            "message":"Lista de aportes por afiliacion",
            "tota_abonos":total_abonos,
            "saldo_actual":saldo_actual,
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=AporteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "message":"Aporte creado exitosamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error de validaciones",
            "errors":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

class AporteDetalle(APIView):
    def patch(self, request, id):
        try:
            aporte=Aporte.objects.get(id=id)
        except Aporte.DoesNotExist:
            return Response({
                "message":"El aporte no existe con ese id"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=AporteSerializer(aporte, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"aporte actualizado correctamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"error de validaciones",
            "errors":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            aporte=Aporte.objects.get(id=id)
        except Aporte.DoesNotExist:
            return Response({
                "message":"no existe el aporte con ese id"
            },status=status.HTTP_404_NOT_FOUND)
        aporte.delete()
        return Response({
            "message":"aporte eliminado exitosamente"
        },status=status.HTTP_200_OK)