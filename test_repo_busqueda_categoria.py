#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.repositories.orm_transportista_repository import TransportistaRepositoryORM
from sigot.infrastructure.db.models import Transportista, TransportistaCategoria

repository = TransportistaRepositoryORM()

# Verificar qué categorías tienen los transportistas
print("=== CATEGORÍAS DE LOS TRANSPORTISTAS ===")
for t in Transportista.objects.all()[:2]:
    print(f"\nTransportista: {t.user.username}")
    tcs = TransportistaCategoria.objects.filter(transportista=t)[:5]
    for tc in tcs:
        print(f"  - Categoría {tc.categoria.id}: {tc.categoria.nombre}")

# Probar búsqueda con categoría 49
print("\n=== BÚSQUEDA CON CATEGORÍA 49 ===")
resultados = repository.find_transportistas_por_zona("29651", category_id=49)
print(f"Encontrados: {len(resultados)} transportistas")

# Verificar si algún transportista tiene la categoría 49
print("\n=== VERIFICAR SI ALGÚN TRANSPORTISTA TIENE CATEGORÍA 49 ===")
tcs_49 = TransportistaCategoria.objects.filter(categoria_id=49)
print(f"TransportistaCategoria con categoría 49: {tcs_49.count()}")
for tc in tcs_49:
    print(f"  - Transportista: {tc.transportista.user.username}")


