from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce
from afiliaciones.models import Afiliacion
from django.utils import timezone


def obtener_afiliaciones(asesor=None, municipio=None, fecha_inicio=None, fecha_fin=None, estado=None):

    afiliaciones = (
        Afiliacion.objects
        .select_related(
            "id_titular",
            "id_asesor",
            "id_titular__id_municipio"
        )
        .filter(
            is_active=True
        )
        .annotate(
            total_abonos=Coalesce(
                Sum("aportes__abono"),
                Value(0),
                output_field=DecimalField(
                    max_digits=15,
                    decimal_places=2
                )
            )
        )
        .annotate(
            saldo=F("valor") - F("total_abonos")
        )
    )

    if asesor:
        afiliaciones = afiliaciones.filter(
            id_asesor_id=asesor
        )

    if municipio:
        afiliaciones = afiliaciones.filter(
            id_titular__id_municipio_id=municipio
        )

    if fecha_inicio and fecha_fin:
            afiliaciones = afiliaciones.filter(
                fecha_fin__range=[fecha_inicio, fecha_fin]
            )
        
    if estado == "vencida":
        afiliaciones = afiliaciones.filter(
            fecha_fin__lt=timezone.now().date()
        )

    elif estado == "vigente":
        afiliaciones = afiliaciones.filter(
            fecha_fin__gte=timezone.now().date()
        )

    return afiliaciones