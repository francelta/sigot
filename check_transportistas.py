#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.db.models import Transportista, TransportistaCategoria

print('=== VERIFICACIÓN DE TRANSPORTISTAS ===\n')
for t in Transportista.objects.all()[:5]:
    print(f'Transportista: {t.user.username}')
    print(f'  - Código Postal: {t.codigo_postal}')
    print(f'  - Radio General: {t.radio_km_general} km')
    print(f'  - Disponible: {t.disponible}')
    print(f'  - Categorías directas: {t.categorias.count()}')
    tc_count = TransportistaCategoria.objects.filter(transportista=t).count()
    print(f'  - TransportistaCategoria (vehículos): {tc_count}')
    if tc_count > 0:
        first_tc = TransportistaCategoria.objects.filter(transportista=t).first()
        print(f'    Ejemplo: {first_tc.categoria.nombre} (Radio: {first_tc.radio_km_especifico} km)')
    print()


