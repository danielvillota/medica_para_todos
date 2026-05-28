from django.urls import path
from aportes.views import AporteView, AporteDetalle

urlpatterns = [
    path('', AporteView.as_view(), name='aporte-creacion'),
    path('afiliacion/<int:afiliacion_id>/', AporteView.as_view(), name='aporte-lista'),
    path('<int:id>/', AporteDetalle.as_view(), name='aporte-detalle'),
]