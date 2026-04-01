import json
from django.core.management.base import BaseCommand
from ubicaciones.models import Municipio, Departamento

class Command(BaseCommand):
    help = 'Carga municipios desde JSON'

    def handle(self, *args, **kwargs):
        with open('ubicaciones/data/cities.json', encoding='utf-8') as file:
            data = json.load(file)

        for mun in data['data']:
            try:
                departamento = Departamento.objects.get(id=mun['departmentId'])
                
                Municipio.objects.update_or_create(
                    id=mun['id'],
                    defaults={
                        'nombre': mun['name'],
                        'id_departamento': departamento
                    }
                )

            except Departamento.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Departamento no encontrado para municipio {mun['name']}"
                    )
                )

        self.stdout.write(self.style.SUCCESS('Municipios cargados correctamente'))