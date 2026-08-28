import json
from django.core.management.base import BaseCommand
from ubicaciones.models import Departamento

class Command(BaseCommand):
    help = 'Carga departamentos desde JSON'

    def handle(self, *args, **kwargs):
        with open('ubicaciones/data/departments.json', encoding='utf-8') as file:
            data = json.load(file)

        for dep in data['data']:  # 👈 CLAVE AQUÍ
            Departamento.objects.update_or_create(
                id=dep['id'],
                defaults={
                    'nombre': dep['name']
                }
            )

        self.stdout.write(self.style.SUCCESS('Departamentos cargados correctamente'))