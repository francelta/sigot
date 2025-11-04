#!/usr/bin/env python
"""
Script para crear un perfil de proveedor para un usuario existente
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from api.models import ProviderProfile

User = get_user_model()

def crear_perfil_proveedor(email):
    """Crear perfil de proveedor para un usuario"""
    try:
        # Buscar el usuario
        user = User.objects.get(email=email)
        
        # Verificar si ya tiene perfil de proveedor
        if hasattr(user, 'provider_profile'):
            print(f"❌ El usuario {email} ya tiene un perfil de proveedor")
            return
        
        # Marcar como proveedor
        user.is_provider = True
        user.save()
        
        # Crear el perfil
        profile = ProviderProfile.objects.create(
            user=user,
            company_name=input("Nombre de la empresa: ") or f"Empresa de {user.first_name or user.username}",
            description="Empresa de maquinaria pesada",
            city=input("Ciudad: ") or "Santiago",
            region=input("Región: ") or "Metropolitana",
            country="Chile",
            subscription_status='active',
            is_verified=True,
            available_within_48h=True
        )
        
        print(f"\n✅ Perfil de proveedor creado exitosamente!")
        print(f"   Usuario: {user.email}")
        print(f"   Empresa: {profile.company_name}")
        print(f"   Ciudad: {profile.city}")
        print(f"   Disponible 48h: {profile.available_within_48h}")
        print(f"\n👉 Ahora puedes agregar maquinaria con este usuario")
        
    except User.DoesNotExist:
        print(f"❌ No existe un usuario con el email: {email}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("🚜 Crear Perfil de Proveedor\n")
    
    # Mostrar usuarios disponibles
    users = User.objects.all()
    print("Usuarios disponibles:")
    for user in users:
        has_provider = "✅ SÍ" if hasattr(user, 'provider_profile') else "❌ NO"
        print(f"  - {user.email} (Perfil proveedor: {has_provider})")
    
    print()
    email = input("Email del usuario para crear perfil de proveedor: ").strip()
    
    if email:
        crear_perfil_proveedor(email)
    else:
        print("❌ Email no puede estar vacío")

