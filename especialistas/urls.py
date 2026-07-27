from django.urls import path
from especialistas.views import EspecialistaView, EspecialistaDetalleView

urlpatterns=[
    path('', EspecialistaView.as_view(), name='especialista-lista-creacion'),
    path('<int:id>/', EspecialistaDetalleView.as_view(), name='especialista-detalle'),
]