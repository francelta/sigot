#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.repositories.orm_transportista_repository import TransportistaRepositoryORM

repository = TransportistaRepositoryORM()

# Probar búsqueda desde 29651 (mismo código postal que los transportistas)
print("=== BÚSQUEDA DESDE 29651 (sin filtro de categoría) ===")
resultados = repository.find_transportistas_por_zona("29651", category_id=None)
print(f"Encontrados: {len(resultados)} transportistas")
for r in resultados[:3]:
    print(f"  - {r.get('user', {}).get('username', 'N/A')}: {r.get('distancia_km', 'N/A')} km")

# Probar búsqueda desde 29651 con filtro de categoría
print("\n=== BÚSQUEDA DESDE 29651 (con categoría 49) ===")
resultados = repository.find_transportistas_por_zona("29651", category_id=49)
print(f"Encontrados: {len(resultados)} transportistas")
for r in resultados[:3]:
    print(f"  - {r.get('user', {}).get('username', 'N/A')}: {r.get('distancia_km', 'N/A')} km")

# Probar búsqueda desde otro código postal cercano
print("\n=== BÚSQUEDA DESDE 29649 (código postal cercano) ===")
resultados = repository.find_transportistas_por_zona("29649", category_id=None)
print(f"Encontrados: {len(resultados)} transportistas")
for r in resultados[:3]:
    print(f"  - {r.get('user', {}).get('username', 'N/A')}: {r.get('distancia_km', 'N/A')} km")


