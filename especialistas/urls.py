from django.urls import path
from especialistas.views import EspecialistaView, EspecialistaDetalleView, EspecialistaOrdenView, EspecialistaOrdenDetalleView, EspecialistaOrdenPDF

urlpatterns=[
    path('', EspecialistaView.as_view(), name='especialista-lista-creacion'),
    path('<int:id>/', EspecialistaDetalleView.as_view(), name='especialista-detalle'),
    path('ordenes/', EspecialistaOrdenView.as_view(), name='orden-lista-creacion'),
    path('orden/<int:id>/', EspecialistaOrdenDetalleView.as_view(), name='orden-detalle'),
    path('orden/<int:id>/pdf/', EspecialistaOrdenPDF.as_view(), name='orden-pdf'),
]