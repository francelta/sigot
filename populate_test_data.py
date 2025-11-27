#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba:
- 5 transportistas con código postal 29651, radio 100km, y al menos un camión por servicio
- 5 clientes con diferentes códigos postales
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.gis.geos import Point as GeoPoint
from geopy.geocoders import Nominatim

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')
django.setup()

from sigot.infrastructure.db.models import User, Transportista, Categoria, TransportistaCategoria

def geocode_postal_code(codigo_postal: str) -> GeoPoint | None:
    """Geocodifica un código postal español."""
    try:
        query = f"{codigo_postal}, España"
        geolocator = Nominatim(user_agent="sigot")
        location = geolocator.geocode(query, timeout=10)
        if location:
            return GeoPoint(location.longitude, location.latitude, srid=4326)
        return None
    except Exception as e:
        print(f"Error geocodificando {codigo_postal}: {e}")
        return None

def create_transportista(username: str, email: str, password: str, codigo_postal: str, radio_km: int = 100):
    """Crea un transportista con su perfil completo."""
    # Crear usuario
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    
    # Calcular trial_end (3 meses desde ahora)
    trial_end = timezone.now() + timedelta(days=90)
    
    # Geocodificar código postal
    base_geocodificada = geocode_postal_code(codigo_postal)
    
    # Crear transportista
    transportista = Transportista.objects.create(
        user=user,
        disponible=True,
        codigo_postal=codigo_postal,
        base_geocodificada=base_geocodificada,
        radio_km_general=radio_km,
        tipo_zona_actuacion='RADIO',
        trial_end=trial_end,
    )
    
    return transportista

def create_cliente(username: str, email: str, password: str, codigo_postal: str):
    """Crea un cliente (usuario no transportista)."""
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    return user

def populate_data():
    """Pobla la base de datos con datos de prueba."""
    print("🗑️  Limpiando datos existentes...")
    User.objects.all().delete()
    Transportista.objects.all().delete()
    
    print("📦 Obteniendo categorías...")
    # Obtener todas las categorías hoja (sin hijos)
    todas_categorias = Categoria.objects.all()
    categorias_hoja = [cat for cat in todas_categorias if not cat.children.exists()]
    
    if not categorias_hoja:
        print("⚠️  No se encontraron categorías. Asegúrate de que las migraciones estén aplicadas.")
        return
    
    print(f"✅ Encontradas {len(categorias_hoja)} categorías hoja")
    
    # Dividir categorías entre los 5 transportistas
    categorias_por_transportista = len(categorias_hoja) // 5
    resto = len(categorias_hoja) % 5
    
    print("\n🚚 Creando 5 transportistas...")
    transportistas_data = [
        {
            'username': 'transportista1',
            'email': 'trans1@test.com',
            'password': 'test1234',
            'codigo_postal': '29651',
        },
        {
            'username': 'transportista2',
            'email': 'trans2@test.com',
            'password': 'test1234',
            'codigo_postal': '29651',
        },
        {
            'username': 'transportista3',
            'email': 'trans3@test.com',
            'password': 'test1234',
            'codigo_postal': '29651',
        },
        {
            'username': 'transportista4',
            'email': 'trans4@test.com',
            'password': 'test1234',
            'codigo_postal': '29651',
        },
        {
            'username': 'transportista5',
            'email': 'trans5@test.com',
            'password': 'test1234',
            'codigo_postal': '29651',
        },
    ]
    
    transportistas = []
    for i, data in enumerate(transportistas_data):
        print(f"  Creando {data['username']}...")
        transportista = create_transportista(**data, radio_km=100)
        transportistas.append(transportista)
        
        # Asignar categorías a este transportista
        inicio = i * categorias_por_transportista
        fin = inicio + categorias_por_transportista
        if i < resto:  # Los primeros transportistas reciben una categoría extra
            fin += 1
        
        categorias_asignadas = categorias_hoja[inicio:fin]
        
        # Crear TransportistaCategoria para cada categoría asignada
        for categoria in categorias_asignadas:
            TransportistaCategoria.objects.create(
                transportista=transportista,
                categoria=categoria,
                radio_km_especifico=100,
                nombre_vehiculo=f"Vehículo {categoria.nombre}",
                marca="Mercedes",
                tonelaje=7.5,
                caracteristicas=f"Vehículo especializado en {categoria.nombre}",
            )
        
        print(f"    ✅ {data['username']} creado con {len(categorias_asignadas)} vehículos")
    
    print("\n👤 Creando 5 clientes...")
    clientes_data = [
        {'username': 'cliente1', 'email': 'cliente1@test.com', 'password': 'test1234', 'codigo_postal': '29649'},
        {'username': 'cliente2', 'email': 'cliente2@test.com', 'password': 'test1234', 'codigo_postal': '29651'},
        {'username': 'cliente3', 'email': 'cliente3@test.com', 'password': 'test1234', 'codigo_postal': '24000'},
        {'username': 'cliente4', 'email': 'cliente4@test.com', 'password': 'test1234', 'codigo_postal': '21000'},
        {'username': 'cliente5', 'email': 'cliente5@test.com', 'password': 'test1234', 'codigo_postal': '31000'},
    ]
    
    for data in clientes_data:
        print(f"  Creando {data['username']}...")
        create_cliente(**data)
        print(f"    ✅ {data['username']} creado")
    
    print("\n" + "="*60)
    print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("="*60)
    print("\n📋 CREDENCIALES DE ACCESO:\n")
    
    print("🚚 TRANSPORTISTAS (Código Postal: 29651, Radio: 100km):")
    for data in transportistas_data:
        print(f"   Usuario: {data['username']}")
        print(f"   Email: {data['email']}")
        print(f"   Password: {data['password']}")
        print()
    
    print("👤 CLIENTES:")
    for data in clientes_data:
        print(f"   Usuario: {data['username']}")
        print(f"   Email: {data['email']}")
        print(f"   Password: {data['password']}")
        print(f"   Código Postal: {data['codigo_postal']}")
        print()
    
    print("="*60)

if __name__ == '__main__':
    populate_data()

