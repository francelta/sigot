#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.db.models import Categoria, TransportistaCategoria

# Obtener categoría 42
cat_42 = Categoria.objects.filter(id=42).first()
print(f"Categoría 42: {cat_42.nombre}")

# Función recursiva para obtener descendientes
def get_all_descendants(cat):
    """Obtiene todas las categorías descendientes recursivamente"""
    descendants = [cat.id]
    for child in cat.children.all():
        descendants.extend(get_all_descendants(child))
    return descendants

# Obtener todas las categorías descendientes de 42
descendants = get_all_descendants(cat_42)
print(f"\nCategorías descendientes de 42: {descendants}")

# Verificar si algún transportista tiene alguna de estas categorías
print("\n=== TRANSPORTISTAS CON CATEGORÍAS DESCENDIENTES DE 42 ===")
for cat_id in descendants:
    tcs = TransportistaCategoria.objects.filter(categoria_id=cat_id)
    if tcs.exists():
        print(f"\nCategoría {cat_id} ({Categoria.objects.get(id=cat_id).nombre}):")
        for tc in tcs:
            print(f"  - {tc.transportista.user.username}")


