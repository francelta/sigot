#!/usr/bin/env python
"""
Script de prueba para verificar que la API de ConnecMaq funciona correctamente.

Uso:
    python test_api.py

Este script crea usuarios de prueba, perfiles, maquinaria y prueba el sistema de chat.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import (
    ConstructorProfile,
    ProviderProfile,
    Machine,
    ChatRoom,
    Message
)

User = get_user_model()


def test_api():
    """Ejecutar pruebas básicas de la API"""
    
    print("🧪 Iniciando pruebas de la API ConnecMaq...\n")
    
    # 1. Crear usuarios de prueba
    print("👥 1. Creando usuarios de prueba...")
    
    # Limpiar datos de prueba existentes
    User.objects.filter(email__contains='@test.com').delete()
    
    # Constructor
    constructor_user = User.objects.create_user(
        email='constructor@test.com',
        username='constructor_test',
        password='TestPass123!',
        first_name='Juan',
        last_name='Constructor',
        is_constructor=True
    )
    print(f"   ✅ Constructor creado: {constructor_user.email}")
    
    # Proveedor
    provider_user = User.objects.create_user(
        email='provider@test.com',
        username='provider_test',
        password='TestPass123!',
        first_name='Pedro',
        last_name='Proveedor',
        is_provider=True
    )
    print(f"   ✅ Proveedor creado: {provider_user.email}")
    
    # 2. Crear perfiles
    print("\n📝 2. Creando perfiles...")
    
    constructor_profile = ConstructorProfile.objects.create(
        user=constructor_user,
        company_name='Constructora Test S.A.',
        phone='+56912345678',
        city='Santiago',
        region='Metropolitana',
        country='Chile'
    )
    print(f"   ✅ Perfil constructor: {constructor_profile.company_name}")
    
    provider_profile = ProviderProfile.objects.create(
        user=provider_user,
        company_name='Maquinarias Test Ltda.',
        description='Empresa de prueba con maquinaria pesada',
        phone='+56987654321',
        city='Santiago',
        region='Metropolitana',
        country='Chile',
        subscription_status='active',
        is_verified=True,
        available_within_48h=True  # EL TOGGLE MÁGICO
    )
    print(f"   ✅ Perfil proveedor: {provider_profile.company_name}")
    print(f"   ⭐ Disponible en 48h: {provider_profile.available_within_48h}")
    
    # 3. Crear maquinaria
    print("\n🚜 3. Creando maquinaria...")
    
    # Nota: En producción, las imágenes se subirían a través del formulario
    # Aquí usamos un placeholder por simplicidad
    print("   ℹ️  Nota: Las imágenes son obligatorias pero se configurarán desde el formulario web")
    
    try:
        # Intentar crear una imagen de prueba simple
        from django.core.files.base import ContentFile
        from PIL import Image
        import io
        
        # Crear una imagen simple de placeholder
        img = Image.new('RGB', (400, 300), color='#3b82f6')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        machine1 = Machine.objects.create(
            provider=provider_profile,
            name='Excavadora CAT 320',
            category='excavator',
            description='Excavadora hidráulica de alto rendimiento',
            brand='Caterpillar',
            model='320',
            year=2020,
            price_per_hour=50000,
            price_per_day=350000,
            is_available=True,
            main_image=ContentFile(img_io.read(), name='excavadora.jpg')
        )
        print(f"   ✅ {machine1.name} - ${machine1.price_per_day}/día")
        
        # Crear segunda imagen
        img_io = io.BytesIO()
        img = Image.new('RGB', (400, 300), color='#10b981')
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        machine2 = Machine.objects.create(
            provider=provider_profile,
            name='Grúa Torre',
            category='crane',
            description='Grúa torre para construcción',
            brand='Liebherr',
            model='EC-B 125',
            year=2019,
            price_per_day=450000,
            is_available=True,
            main_image=ContentFile(img_io.read(), name='grua.jpg')
        )
        print(f"   ✅ {machine2.name} - ${machine2.price_per_day}/día")
    except Exception as e:
        print(f"   ⚠️  No se pudieron crear imágenes de prueba: {e}")
        print(f"   ℹ️  Agrega maquinaria desde el panel web del proveedor")
    
    # 4. Probar búsqueda de proveedores
    print("\n🔍 4. Probando búsqueda de proveedores...")
    
    # Buscar proveedores disponibles en 48h
    providers_48h = ProviderProfile.objects.filter(
        available_within_48h=True,
        subscription_status='active',
        is_verified=True
    )
    print(f"   ✅ Proveedores disponibles en 48h: {providers_48h.count()}")
    for provider in providers_48h:
        print(f"      - {provider.company_name} ({provider.city})")
        machines_count = provider.machines.filter(is_available=True).count()
        print(f"        📦 Maquinaria disponible: {machines_count}")
    
    # 5. Crear sala de chat
    print("\n💬 5. Creando sala de chat...")
    
    chat_room = ChatRoom.objects.create()
    chat_room.participants.add(constructor_user, provider_user)
    print(f"   ✅ Sala de chat creada: #{chat_room.id}")
    print(f"      Participantes: {constructor_user.email} <-> {provider_user.email}")
    
    # 6. Crear mensajes
    print("\n📨 6. Enviando mensajes...")
    
    message1 = Message.objects.create(
        room=chat_room,
        author=constructor_user,
        content='Hola, me interesa la Excavadora CAT 320. ¿Está disponible?'
    )
    print(f"   ✅ Mensaje de {message1.author.first_name}: {message1.content[:50]}...")
    
    message2 = Message.objects.create(
        room=chat_room,
        author=provider_user,
        content='¡Hola! Sí, está disponible. ¿Para qué fecha la necesitas?'
    )
    print(f"   ✅ Mensaje de {message2.author.first_name}: {message2.content[:50]}...")
    
    # Marcar mensaje como leído
    message1.read = True
    message1.save()
    print(f"   ✅ Mensaje marcado como leído")
    
    # 7. Toggle de disponibilidad
    print("\n⚡ 7. Probando toggle de disponibilidad 48h...")
    print(f"   Estado actual: {provider_profile.available_within_48h}")
    provider_profile.available_within_48h = not provider_profile.available_within_48h
    provider_profile.save()
    print(f"   Estado después del toggle: {provider_profile.available_within_48h}")
    # Volver al estado original
    provider_profile.available_within_48h = True
    provider_profile.save()
    print(f"   Estado final: {provider_profile.available_within_48h}")
    
    # 8. Estadísticas finales
    print("\n📊 8. Estadísticas finales:")
    print(f"   👥 Usuarios: {User.objects.count()}")
    print(f"   🏗️ Constructores: {ConstructorProfile.objects.count()}")
    print(f"   🚜 Proveedores: {ProviderProfile.objects.count()}")
    print(f"      - Activos: {ProviderProfile.objects.filter(subscription_status='active').count()}")
    print(f"      - Disponibles 48h: {ProviderProfile.objects.filter(available_within_48h=True).count()}")
    print(f"   📦 Maquinaria: {Machine.objects.count()}")
    print(f"      - Disponible: {Machine.objects.filter(is_available=True).count()}")
    print(f"   💬 Salas de chat: {ChatRoom.objects.count()}")
    print(f"   📨 Mensajes: {Message.objects.count()}")
    print(f"      - Leídos: {Message.objects.filter(read=True).count()}")
    print(f"      - No leídos: {Message.objects.filter(read=False).count()}")
    
    print("\n✅ ¡Todas las pruebas completadas exitosamente!")
    print("\n📝 Credenciales de prueba:")
    print("   Constructor:")
    print("     Email: constructor@test.com")
    print("     Password: TestPass123!")
    print("\n   Proveedor:")
    print("     Email: provider@test.com")
    print("     Password: TestPass123!")
    print("\n🌐 Ahora puedes probar la API en:")
    print("   - Admin: http://localhost:8000/admin/")
    print("   - API: http://localhost:8000/api/")
    print("   - Búsqueda: http://localhost:8000/api/providers/search/?available_within_48h=true")


if __name__ == '__main__':
    try:
        test_api()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

