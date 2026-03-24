from django.urls import path
from users.views import UsuarioView, UsuarioDetalleView

urlpatterns=[
    path('', UsuarioView.as_view(), name='usuarios-lista-creacion'),
    path('<int:id>/', UsuarioDetalleView.as_view(), name='usuario-detalle'),
]