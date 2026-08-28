from django.urls import path
from beneficiarios.views import BeneficiarioView, BeneficiarioDetalleView, BeneficiarioTitularView

urlpatterns=[
    path('', BeneficiarioView.as_view(), name='beneficiario-lista-creacion'),
    path('<int:id>/', BeneficiarioDetalleView.as_view(), name='beneficiario-detalle'),
    path('titular/<int:titular_id>/', BeneficiarioTitularView.as_view(), name='beneficiario-titular'),
]