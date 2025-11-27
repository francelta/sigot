#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.db.models import Transportista
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
from geopy.geocoders import Nominatim

# Geocodificar 29651
geolocator = Nominatim(user_agent="sigot")
location = geolocator.geocode("29651, España", timeout=10)
if location:
    cliente_point = GeoPoint(location.longitude, location.latitude, srid=4326)
else:
    print("No se pudo geocodificar")
    sys.exit(1)

# Construir la consulta exactamente como en el repositorio
queryset = Transportista.objects.filter(disponible=True).select_related('user').prefetch_related(
    'categorias', 'transportistacategoria_set', 'transportistacategoria_set__categoria'
)

print(f"Total transportistas disponibles: {queryset.count()}")

# Caso 1: Transportistas con RADIO
radio_filter = Q(
    tipo_zona_actuacion='RADIO',
    base_geocodificada__isnull=False,
) & (
    Q(radio_km_general__isnull=False) | 
    Q(transportistacategoria_set__radio_km_especifico__isnull=False)
)

print(f"\nFiltro aplicado:")
print(f"  - tipo_zona_actuacion='RADIO': {Transportista.objects.filter(tipo_zona_actuacion='RADIO').count()}")
print(f"  - base_geocodificada__isnull=False: {Transportista.objects.filter(base_geocodificada__isnull=False).count()}")
print(f"  - radio_km_general__isnull=False: {Transportista.objects.filter(radio_km_general__isnull=False).count()}")
print(f"  - transportistacategoria_set__radio_km_especifico__isnull=False: {Transportista.objects.filter(transportistacategoria_set__radio_km_especifico__isnull=False).count()}")

queryset_radio = queryset.filter(radio_filter).annotate(
    distance=Distance('base_geocodificada', cliente_point)
).distinct()

print(f"\nTransportistas después del filtro: {queryset_radio.count()}")

resultados = []
for transportista in queryset_radio:
    radio_efectivo = transportista.radio_km_general
    print(f"\n  Transportista: {transportista.user.username}")
    print(f"    Distancia: {transportista.distance.km:.2f} km")
    print(f"    Radio efectivo: {radio_efectivo} km")
    
    if not radio_efectivo:
        print(f"    ❌ Saltado: no tiene radio efectivo")
        continue
    
    if transportista.distance.km <= radio_efectivo:
        print(f"    ✅ Añadido a resultados")
        resultados.append(transportista)
    else:
        print(f"    ❌ Saltado: fuera del radio")

print(f"\nTotal resultados: {len(resultados)}")


