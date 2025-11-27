#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.repositories.orm_transportista_repository import TransportistaRepositoryORM

repository = TransportistaRepositoryORM()

print("=== BÚSQUEDA CON CATEGORÍA 42 (Áridos, Construcción y Residuos) ===")
resultados = repository.find_transportistas_por_zona("29651", category_id=42)
print(f"Resultados: {len(resultados)} transportistas")
for r in resultados[:5]:
    print(f"  - {r.get('user', {}).get('username', 'N/A')}: {r.get('distancia_km', 'N/A')} km")


