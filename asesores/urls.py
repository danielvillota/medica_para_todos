from django.urls import path
from asesores.views import AsesorView, AsesorDetalleView

urlpatterns=[
    path('', AsesorView.as_view(), name='asesor-lista-creacion'),
    path('<int:id>/', AsesorDetalleView.as_view(), name='asesor-detalle'),
]