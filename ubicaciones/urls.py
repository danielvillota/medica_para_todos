from django.urls import path
from ubicaciones.views import DepartamentoView, MunicipioView

urlpatterns=[
    path('', DepartamentoView.as_view(), name='departamentos-lista'),
    path('<int:id_departamento>/', MunicipioView.as_view(), name='municipios-lista'),
]