#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.db.models import Transportista, TransportistaCategoria, Categoria

# Verificar categoría 42
cat_42 = Categoria.objects.filter(id=42).first()
print(f"Categoría 42: {cat_42.nombre if cat_42 else 'No existe'}")

# Verificar qué transportistas tienen categoría 42
print("\n=== TRANSPORTISTAS CON CATEGORÍA 42 ===")
tcs_42 = TransportistaCategoria.objects.filter(categoria_id=42)
print(f"Total: {tcs_42.count()}")
for tc in tcs_42:
    print(f"  - {tc.transportista.user.username}")

# Verificar todas las categorías de los primeros 2 transportistas
print("\n=== CATEGORÍAS DE LOS PRIMEROS 2 TRANSPORTISTAS ===")
for t in Transportista.objects.all()[:2]:
    print(f"\n{t.user.username}:")
    tcs = TransportistaCategoria.objects.filter(transportista=t)[:10]
    for tc in tcs:
        print(f"  - Cat {tc.categoria.id}: {tc.categoria.nombre}")
    print(f"  ¿Tiene categoría 42? {TransportistaCategoria.objects.filter(transportista=t, categoria_id=42).exists()}")


