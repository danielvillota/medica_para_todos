from django.urls import path
from afiliaciones.views import AfiliacionView, AfiliacionDetalleView

urlpatterns=[
    path('', AfiliacionView.as_view(), name='afiliacion-lista-creacion'),
    path('<int:id>/', AfiliacionDetalleView.as_view(), name='afiliacion-detalle')
]