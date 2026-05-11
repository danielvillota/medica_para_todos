from django.urls import path
from beneficiarios.views import BeneficiarioView, BeneficiarioDetalleView

urlpatterns=[
    path('', BeneficiarioView.as_view(), name='beneficiario-lista-creacion'),
    path('<int:id>/', BeneficiarioDetalleView.as_view(), name='beneficiario-detalle'),
]