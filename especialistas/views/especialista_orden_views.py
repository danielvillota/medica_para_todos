from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from especialistas.models import Orden
from especialistas.serializers import EspecialistaOrdenSerializer
from paginacion.paginacion import Paginacion
from django.template.loader import render_to_string
from utils.images import get_static_image_base64
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse

class EspecialistaOrdenView(APIView):
    def post(self, request):
        serializer=EspecialistaOrdenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Orden creada correctamnete",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)
        return Response({
            "message":"Error en validaciones",
            "erros":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        ordenes=Orden.objects.all()
        paginador=Paginacion()
        pagina=paginador.paginate_queryset(
            ordenes,
            request
        )
        serializer=EspecialistaOrdenSerializer(pagina, many=True)
        return paginador.get_paginated_response(
            serializer.data
        )

class EspecialistaOrdenDetalleView(APIView):
    def get(self, request, id):
        try:
            orden=Orden.objects.get(id=id)
        except Orden.DoesNotExist:
            return Response({
                "message":"la orden no existe"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=EspecialistaOrdenSerializer(orden)
        return Response({
            "message":"detalle de la orden",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        try:
            orden=Orden.objects.get(id=id)
        except Orden.DoesNotExist:
            return Response({
                "message":"la orden no existe"
            },status=status.HTTP_404_NOT_FOUND)
        serializer=EspecialistaOrdenSerializer(orden, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"orden actualizado correctamente",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            "message":"error de validaciones",
            "error":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            orden=Orden.objects.get(id=id)
        except Orden.DoesNotExist:
            return Response({
                "message":"la orden no existe"
            },status=status.HTTP_404_NOT_FOUND)
        orden.delete()
        return Response({
            "message":"orden eliminada exitosamente"
        },status=status.HTTP_200_OK)
        
class EspecialistaOrdenPDF(APIView):
    def get(self, request, id):
        orden=Orden.objects.get(id=id)
        logo_base64 = get_static_image_base64(
            "especialistas/img/logo.svg"
        )
        context={
            "logo":logo_base64,
            "contrato": orden.contrato,
            "afiliado": orden.afiliado,
            "celular": orden.celular,
            "nombre_especialista": orden.nombre_especialista,
            "especialidad": orden.especialidad,
            "estado_cita": orden.estado_cita,
            "particular": f"${orden.particular:,.0f}",
            "descuento": f"${orden.descuento:,.0f}",
            "direccion": orden.direccion,
            "observacion_cita": orden.observacion_cita,
            "fecha_cita": orden.fecha_cita,
            "hora": orden.hora,
            "secretaria": orden.secretaria,
        }
        html = render_to_string(
            "ordenes/orden_medica.html",
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

        response["Content-Disposition"] = 'inline; filename="orden_medica.pdf"'

        return response