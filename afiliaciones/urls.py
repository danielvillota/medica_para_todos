from django.urls import path
from afiliaciones.views import AfiliacionView, AfiliacionDetalleView, AfiliacionCarnetView, AfiliacionReporteView, AfiliacionReportePDFView

urlpatterns=[
    path('', AfiliacionView.as_view(), name='afiliacion-lista-creacion'),
    path('<int:id>/', AfiliacionDetalleView.as_view(), name='afiliacion-detalle'),
    path('<int:id>/carnet/', AfiliacionCarnetView.as_view(), name='afiliacion-carnet'),
    path('reporte/', AfiliacionReporteView.as_view(), name='afiliacion-reporte'),
    path('reporte/pdf/', AfiliacionReportePDFView.as_view(), name='afiliacion-reporte-pdf'),
]