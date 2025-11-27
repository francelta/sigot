# Generated migration for loading categorías

from django.db import migrations


def load_categorias(apps, schema_editor):
    """
    Carga la jerarquía completa de categorías de transporte.
    
    Esta es la ÚNICA fuente de verdad para las categorías del sistema.
    Soporta jerarquías de N-niveles mediante relaciones parent-child.
    
    Estructura:
    - Nivel 1: Categorías principales (raíz)
    - Nivel 2: Subcategorías
    - Nivel 3+: Sub-subcategorías (profundidad arbitraria)
    """
    Categoria = apps.get_model('db', 'Categoria')
    
    # Definición de la jerarquía completa
    # Formato: (nombre, descripcion, parent_nombre, nivel)
    categorias_data = [
        # ============================================================
        # NIVEL 1: CATEGORÍAS RAÍZ
        # ============================================================
        ('Mercancías', 'Transporte de mercancías y carga general', None, 1),
        ('Maquinaria', 'Transporte de maquinaria pesada y equipos', None, 1),
        ('Mecánicos', 'Servicios de mecánica y reparación', None, 1),
        ('Especializados', 'Transportes especializados y servicios únicos', None, 1),
        
        # ============================================================
        # NIVEL 2: SUBCATEGORÍAS DE MERCADURÍAS
        # ============================================================
        ('Mercancías Generales', 'Carga general y pallets', 'Mercancías', 2),
        ('Mercancías Peligrosas', 'Materiales peligrosos (ADR)', 'Mercancías', 2),
        ('Mercancías Frigoríficas', 'Transporte refrigerado y congelado', 'Mercancías', 2),
        ('Mercancías a Granel', 'Carga a granel y líquidos', 'Mercancías', 2),
        
        # ============================================================
        # NIVEL 3: SUB-SUBCATEGORÍAS DE MERCADURÍAS PELIGROSAS
        # ============================================================
        ('Explosivos', 'Materiales explosivos (Clase 1 ADR)', 'Mercancías Peligrosas', 3),
        ('Gases', 'Gases comprimidos, licuados o disueltos (Clase 2 ADR)', 'Mercancías Peligrosas', 3),
        ('Líquidos Inflamables', 'Líquidos inflamables (Clase 3 ADR)', 'Mercancías Peligrosas', 3),
        ('Sólidos Inflamables', 'Sólidos inflamables (Clase 4 ADR)', 'Mercancías Peligrosas', 3),
        ('Sustancias Oxidantes', 'Sustancias comburentes y peróxidos (Clase 5 ADR)', 'Mercancías Peligrosas', 3),
        ('Sustancias Tóxicas', 'Sustancias tóxicas e infecciosas (Clase 6 ADR)', 'Mercancías Peligrosas', 3),
        ('Materiales Radiactivos', 'Materiales radiactivos (Clase 7 ADR)', 'Mercancías Peligrosas', 3),
        ('Sustancias Corrosivas', 'Sustancias corrosivas (Clase 8 ADR)', 'Mercancías Peligrosas', 3),
        ('Sustancias y Objetos Peligrosos', 'Sustancias y objetos peligrosos varios (Clase 9 ADR)', 'Mercancías Peligrosas', 3),
        
        # ============================================================
        # NIVEL 2: SUBCATEGORÍAS DE MAQUINARIA
        # ============================================================
        ('Maquinaria Agrícola', 'Tractores, cosechadoras y equipos agrícolas', 'Maquinaria', 2),
        ('Maquinaria de Construcción', 'Excavadoras, grúas y equipos de construcción', 'Maquinaria', 2),
        ('Maquinaria Industrial', 'Equipos industriales y de producción', 'Maquinaria', 2),
        ('Vehículos Pesados', 'Camiones, autobuses y vehículos comerciales', 'Maquinaria', 2),
        
        # ============================================================
        # NIVEL 3: SUB-SUBCATEGORÍAS DE MAQUINARIA DE CONSTRUCCIÓN
        # ============================================================
        ('Excavadoras', 'Excavadoras y retroexcavadoras', 'Maquinaria de Construcción', 3),
        ('Grúas', 'Grúas móviles y torre', 'Maquinaria de Construcción', 3),
        ('Bulldozers', 'Bulldozers y niveladoras', 'Maquinaria de Construcción', 3),
        ('Compactadoras', 'Rodillos y compactadoras', 'Maquinaria de Construcción', 3),
        
        # ============================================================
        # NIVEL 2: SUBCATEGORÍAS DE MECÁNICOS
        # ============================================================
        ('Mecánica General', 'Reparaciones y mantenimiento general', 'Mecánicos', 2),
        ('Mecánica Especializada', 'Reparaciones especializadas y diagnósticos', 'Mecánicos', 2),
        ('Mantenimiento Preventivo', 'Servicios de mantenimiento programado', 'Mecánicos', 2),
        ('Emergencias Mecánicas', 'Servicio de asistencia en carretera', 'Mecánicos', 2),
        
        # ============================================================
        # NIVEL 2: SUBCATEGORÍAS DE ESPECIALIZADOS
        # ============================================================
        ('Transporte de Animales', 'Transporte de ganado y animales vivos', 'Especializados', 2),
        ('Transporte de Obras de Arte', 'Transporte seguro de obras de arte y antigüedades', 'Especializados', 2),
        ('Transporte de Mudanzas', 'Servicios de mudanza y traslados', 'Especializados', 2),
        ('Transporte de Vehículos', 'Transporte de coches y motocicletas', 'Especializados', 2),
    ]
    
    # Diccionario para mapear nombres a objetos Categoria
    categorias_dict = {}
    
    # Crear categorías nivel por nivel
    for nivel in [1, 2, 3, 4, 5]:  # Soporta hasta 5 niveles
        for nombre, descripcion, parent_nombre, nivel_data in categorias_data:
            if nivel_data != nivel:
                continue
            
            # Obtener el parent si existe
            parent = None
            if parent_nombre:
                parent = categorias_dict.get(parent_nombre)
                if not parent:
                    # Si el parent no existe, saltar esta categoría (se creará en el siguiente nivel)
                    continue
            
            # Crear la categoría si no existe
            if nombre not in categorias_dict:
                categoria, created = Categoria.objects.get_or_create(
                    nombre=nombre,
                    defaults={
                        'descripcion': descripcion,
                        'parent': parent,
                    }
                )
                categorias_dict[nombre] = categoria
            else:
                # Actualizar si ya existe
                categoria = categorias_dict[nombre]
                if categoria.parent != parent:
                    categoria.parent = parent
                    categoria.descripcion = descripcion
                    categoria.save()


def reverse_load_categorias(apps, schema_editor):
    """Elimina todas las categorías cargadas."""
    Categoria = apps.get_model('db', 'Categoria')
    Categoria.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_categorias, reverse_load_categorias),
    ]
