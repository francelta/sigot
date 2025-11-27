#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.repositories.orm_transportista_repository import TransportistaRepositoryORM

repository = TransportistaRepositoryORM()

# Probar búsqueda directamente
print("=== BÚSQUEDA DIRECTA DESDE EL REPOSITORIO ===")
print("Buscando desde '29651' sin filtro de categoría...")
resultados = repository.find_transportistas_por_zona("29651", category_id=None)
print(f"Resultados: {len(resultados)}")
if resultados:
    print(f"Primer resultado: {resultados[0].get('user', {}).get('username', 'N/A')}")
    print(f"  - ID: {resultados[0].get('id', 'N/A')}")
    print(f"  - Distancia: {resultados[0].get('distancia_km', 'N/A')} km")
else:
    print("❌ No se encontraron resultados")


