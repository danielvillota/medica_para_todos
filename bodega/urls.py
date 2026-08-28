from django.urls import path
from bodega.views import PapeleriaView, PapeleriaDetalleView

urlpatterns = [
    path('', PapeleriaView.as_view(), name='papeleria-creacion-lista'),
    path('<int:id>/', PapeleriaDetalleView.as_view(), name='papeleria-detalle'),
]
