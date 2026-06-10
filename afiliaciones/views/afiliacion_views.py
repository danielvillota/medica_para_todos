from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from afiliaciones.models import Afiliacion
from afiliaciones.serializers import AfiliacionSerializer
from django.db.models import Q
from paginacion.paginacion import Paginacion

class AfiliacionView(APIView):
    def post(self, request):
        serializer=AfiliacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Afiliacion creada exitosamente",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        contrato = request.query_params.get('contrato')
        provisional = request.query_params.get('provisional')
        nombre = request.query_params.get('nombre')
        cedula = request.query_params.get('cedula')
        afiliaciones=Afiliacion.objects.select_related('id_titular').all()
        if contrato:
            afiliaciones = afiliaciones.filter(
                contrato__icontains=contrato
            )
        if provisional:
            afiliaciones = afiliaciones.filter(
                provisional__icontains=provisional
            )
        if nombre:
            afiliaciones = afiliaciones.filter(
                id_titular__nombre__icontains=nombre
            )
        if cedula:
            afiliaciones = afiliaciones.filter(
                id_titular__cedula__icontains=cedula
            )
        paginador=Paginacion()
        pagina = paginador.paginate_queryset(
            afiliaciones,
            request
        )
        serializer=AfiliacionSerializer(pagina, many=True)
        return paginador.get_paginated_response(
            serializer.data
        )

class AfiliacionDetalleView(APIView):
    def get(self, reuqest, id):
        try:
            afiliacion=Afiliacion.objects.get(id=id)
        except Afiliacion.DoesNotExist:
            return Response({
                "message":"La afiliacion no existe",
            },status=status.HTTP_404_NOT_FOUND)
        serializer=AfiliacionSerializer(afiliacion)
        return Response({
            "message":"Detalle afiliacion",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        try:
            afiliacion=Afiliacion.objects.get(id=id)
        except Afiliacion.DoesNotExist:
            return Response({
                "message":"la afiliacion no existe"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=AfiliacionSerializer(afiliacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Afiliacion actualizada exitosamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"Error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, reuqest, id):
        try:
            afiliacion=Afiliacion.objects.get(id=id)
        except Afiliacion.DoesNotExist:
            return Response({
                "message":"No existe la afiliacion"
            },status=status.HTTP_404_NOT_FOUND)
        afiliacion.is_active=False
        afiliacion.save()
        return Response({
            "message":"Afiliacion desactivada exitosamente"
        },status=status.HTTP_200_OK)
        