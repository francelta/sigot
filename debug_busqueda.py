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
from geopy.geocoders import Nominatim

# Geocodificar 29651
geolocator = Nominatim(user_agent="sigot")
location = geolocator.geocode("29651, España", timeout=10)
if location:
    cliente_point = GeoPoint(location.longitude, location.latitude, srid=4326)
    print(f"Punto cliente (29651): {cliente_point}")
else:
    print("No se pudo geocodificar 29651")
    sys.exit(1)

# Obtener transportistas
transportistas = Transportista.objects.filter(disponible=True).select_related('user').prefetch_related(
    'categorias', 'transportistacategoria_set', 'transportistacategoria_set__categoria'
)

print(f"\nTotal transportistas disponibles: {transportistas.count()}")

# Verificar cada transportista
for t in transportistas[:3]:
    print(f"\n--- Transportista: {t.user.username} ---")
    print(f"Base geocodificada: {t.base_geocodificada}")
    print(f"Radio general: {t.radio_km_general} km")
    print(f"Tipo zona: {t.tipo_zona_actuacion}")
    
    if t.base_geocodificada:
        # Calcular distancia
        from django.db.models import F
        t_with_dist = Transportista.objects.filter(user_id=t.user_id).annotate(
            distance=Distance('base_geocodificada', cliente_point)
        ).first()
        
        if t_with_dist and hasattr(t_with_dist, 'distance'):
            distancia_km = t_with_dist.distance.km
            print(f"Distancia al cliente: {distancia_km:.2f} km")
            print(f"Radio efectivo: {t.radio_km_general} km")
            print(f"¿Está dentro del radio? {distancia_km <= (t.radio_km_general or 0)}")
        else:
            print("No se pudo calcular la distancia")

