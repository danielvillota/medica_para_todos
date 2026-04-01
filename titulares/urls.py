from django.urls import path
from titulares.views import TitularView, TitularDetalleView

urlpatterns=[
    path('', TitularView.as_view(), name='titular-lista-creacion'),
    path('<int:id>/', TitularDetalleView.as_view(), name='titular-detalle'),
]