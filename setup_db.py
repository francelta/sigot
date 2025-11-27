#!/usr/bin/env python3
"""
Script para crear la base de datos SIGOT con PostGIS
Uso: python setup_db.py
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración (puedes cambiarla con variables de entorno)
DB_NAME = os.environ.get('DB_NAME', 'sigot')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')

def main():
    print("🗄️  Configurando base de datos SIGOT...")
    print(f"   Base de datos: {DB_NAME}")
    print(f"   Usuario: {DB_USER}")
    print(f"   Host: {DB_HOST}:{DB_PORT}")
    print()

    # Conectar a PostgreSQL (base de datos 'postgres' por defecto)
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
    except psycopg2.OperationalError as e:
        print(f"❌ Error: No se pudo conectar a PostgreSQL")
        print(f"   {e}")
        print()
        print("Asegúrate de que PostgreSQL esté corriendo:")
        print("  - macOS: brew services start postgresql")
        print("  - Linux: sudo systemctl start postgresql")
        print("  - Docker: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgis/postgis")
        sys.exit(1)

    print("✅ Conectado a PostgreSQL")

    # Verificar si la base de datos existe
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )
    exists = cursor.fetchone()

    if not exists:
        # Crear la base de datos
        print(f"📦 Creando base de datos '{DB_NAME}'...")
        try:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"✅ Base de datos '{DB_NAME}' creada")
        except psycopg2.Error as e:
            print(f"❌ Error al crear la base de datos: {e}")
            cursor.close()
            conn.close()
            sys.exit(1)
    else:
        print(f"ℹ️  La base de datos '{DB_NAME}' ya existe")

    cursor.close()
    conn.close()

    # Conectar a la nueva base de datos para habilitar PostGIS
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
    except psycopg2.Error as e:
        print(f"❌ Error al conectar a la base de datos '{DB_NAME}': {e}")
        sys.exit(1)

    # Habilitar PostGIS
    print("🗺️  Habilitando extensión PostGIS...")
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
        print("✅ PostGIS habilitado")
    except psycopg2.Error as e:
        print(f"❌ Error al habilitar PostGIS: {e}")
        print()
        print("Asegúrate de que PostGIS esté instalado:")
        print("  - macOS: brew install postgis")
        print("  - Linux: sudo apt-get install postgis")
        print("  - Docker: Usa la imagen postgis/postgis")
        cursor.close()
        conn.close()
        sys.exit(1)

    cursor.close()
    conn.close()

    print()
    print("🎉 Base de datos configurada correctamente!")
    print()
    print("Próximos pasos:")
    print("  python manage.py migrate")
    print("  python manage.py runserver")

if __name__ == '__main__':
    main()


