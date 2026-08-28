from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from afiliaciones.models import Afiliacion
from afiliaciones.serializers import AfiliacionSerializer, AfiliacionCarnetSerializer, AfiliacionReporteSerializer
from django.db.models import Q
from paginacion.paginacion import Paginacion
from django.db.models import Sum, F, DecimalField, Value
from django.db.models.functions import Coalesce
from afiliaciones.services.reporte_service import obtener_afiliaciones
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.utils import timezone

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

class AfiliacionCarnetView(APIView):
    def get(self, request, id):
        try:
            afiliacion = (
                Afiliacion.objects
                .select_related(
                    'id_titular',
                    'id_asesor'
                )
                .prefetch_related(
                    'id_titular__beneficiarios'
                )
                .get(id=id)
            )

        except Afiliacion.DoesNotExist:
            return Response({
                "message": "No existe la afiliación"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AfiliacionCarnetSerializer(afiliacion)

        return Response({
            "message": "Datos de afiliacion",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
class AfiliacionReporteView(APIView):
    def get(self, request):
        asesor=request.query_params.get('asesor')
        municipio=request.query_params.get('municipio')
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")
        estado = request.query_params.get("estado")
        afiliaciones=(Afiliacion.objects.select_related(
            "id_titular",
            "id_asesor",
            "id_titular__id_municipio"
        )
        .filter(
            is_active=True
        )
        .annotate(
            total_abonos=Coalesce(
                Sum("aportes__abono"),
                Value(0),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
        .annotate(
            saldo=F("valor") - F("total_abonos")
        )
        )
        
        if asesor:
            afiliaciones = afiliaciones.filter(
                id_asesor_id=asesor
            )

        if municipio:
            afiliaciones = afiliaciones.filter(
                id_titular__id_municipio_id=municipio
            )
        
        
        if fecha_inicio and fecha_fin:
            afiliaciones = afiliaciones.filter(
                fecha_fin__range=[fecha_inicio, fecha_fin]
            )
        
        if estado == "vencida":
            afiliaciones = afiliaciones.filter(
                fecha_fin__lt=timezone.now().date()
            )

        elif estado == "vigente":
            afiliaciones = afiliaciones.filter(
                fecha_fin__gte=timezone.now().date()
            )
        
        paginador=Paginacion()
        pagina=paginador.paginate_queryset(afiliaciones, request)
        
        serializer=AfiliacionReporteSerializer(pagina, many=True)
        
        return paginador.get_paginated_response(
            serializer.data
        )

class AfiliacionReportePDFView(APIView):

    def get(self, request):

        asesor = request.query_params.get("asesor")
        municipio = request.query_params.get("municipio")
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")
        estado = request.query_params.get("estado")

        afiliaciones = obtener_afiliaciones(
            asesor,
            municipio,
            fecha_inicio,
            fecha_fin,
            estado
        )

        serializer = AfiliacionReporteSerializer(
            afiliaciones,
            many=True
        )

        context = {
            "afiliaciones": serializer.data
        }

        html = render_to_string(
            "afiliaciones/reporte_afiliaciones.html",
            context
        )

        result = BytesIO()

        pdf = pisa.CreatePDF(
            html,
            dest=result
        )

        if pdf.err:
            return HttpResponse(
                "Error al generar PDF",
                status=500
            )

        response = HttpResponse(
            result.getvalue(),
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = 'inline; filename="reporte_afiliaciones.pdf"'

        return response