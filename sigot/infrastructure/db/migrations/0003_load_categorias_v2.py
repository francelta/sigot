# Generated migration for loading categorías v2.0 (Taxonomía Definitiva de SIGOT)

from django.db import migrations


def load_categorias_v2(apps, schema_editor):
    """
    Carga la Taxonomía Definitiva de SIGOT (v2.0).
    
    Esta es la ÚNICA fuente de verdad para las categorías del sistema.
    Soporta jerarquías de N-niveles mediante relaciones parent-child.
    
    Estructura completa según la Taxonomía Definitiva de SIGOT (v2.0):
    - 5 categorías raíz principales
    - Múltiples niveles de anidación (hasta 4-5 niveles en algunos casos)
    """
    Categoria = apps.get_model('db', 'Categoria')
    
    # Primero, eliminar todas las categorías existentes (si las hay)
    Categoria.objects.all().delete()
    
    # Definición de la jerarquía completa según Taxonomía v2.0
    # Formato: (nombre, descripcion, parent_nombre, nivel)
    categorias_data = [
        # ============================================================
        # 1. TRANSPORTE DE MERCADURÍAS
        # ============================================================
        ('Transporte de Mercancías', 'Transporte de mercancías y carga general', None, 1),
        
        # 1.1. Carga General (Seca)
        ('Carga General (Seca)', 'Carga general seca y pallets', 'Transporte de Mercancías', 2),
        ('Transporte Ligero (Furgoneta / Carrozado)', 'Transporte ligero con furgoneta o carrozado', 'Carga General (Seca)', 3),
        ('Camión Paquetero', 'Camión especializado en paquetería', 'Carga General (Seca)', 3),
        ('Camión <= 3500kg', 'Camión chasis-cabina, plataforma, etc. hasta 3500kg', 'Carga General (Seca)', 3),
        ('Camión Rígido', 'Camión rígido de 2 y 3 ejes > 3500kg', 'Carga General (Seca)', 3),
        ('Camión Articulado (Tráiler)', 'Tráiler articulado para carga general', 'Carga General (Seca)', 3),
        ('Tráiler Lona (Tauliner)', 'Tráiler con lona (tauliner)', 'Camión Articulado (Tráiler)', 4),
        ('Tráiler Plataforma (Plana)', 'Tráiler plataforma plana', 'Camión Articulado (Tráiler)', 4),
        ('Tráiler Portabobinas', 'Tráiler especializado para bobinas', 'Camión Articulado (Tráiler)', 4),
        
        # 1.2. Temperatura Controlada
        ('Temperatura Controlada', 'Transporte con control de temperatura', 'Transporte de Mercancías', 2),
        ('Camión Frigorífico', 'Camión frigorífico (refrigerado / congelado)', 'Temperatura Controlada', 3),
        ('Camión Isotermo', 'Camión isotermo sin equipo de frío', 'Temperatura Controlada', 3),
        
        # 1.3. Cisternas (Líquidos, Polvos, Gases)
        ('Cisternas (Líquidos, Polvos, Gases)', 'Transporte en cisternas', 'Transporte de Mercancías', 2),
        ('Camión Cubas', 'Camión cubas (término genérico, p.ej. agua)', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        ('Cisterna de Agua', 'Cisterna de agua (riego, potable, no potable)', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        ('Cisterna de Combustible / ADR', 'Cisterna de combustible con certificación ADR', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        ('Cisterna Alimentaria', 'Cisterna para productos alimentarios (leche, vino, aceite)', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        ('Cisterna Pulverulentos', 'Cisterna para pulverulentos (cemento, harina, pienso)', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        ('Cisterna de Gases', 'Cisterna de gases (GLP, GNL, criogénicos)', 'Cisternas (Líquidos, Polvos, Gases)', 3),
        
        # 1.4. Áridos, Construcción y Residuos
        ('Áridos, Construcción y Residuos', 'Transporte de áridos, construcción y residuos', 'Transporte de Mercancías', 2),
        ('Camión Basculante (Volquete)', 'Camión basculante volquete (2/3 ejes)', 'Áridos, Construcción y Residuos', 3),
        ('Camión Portacontenedores', 'Camión portacontenedores (gancho / multilift)', 'Áridos, Construcción y Residuos', 3),
        ('Bañera', 'Semirremolque basculante (bañera)', 'Áridos, Construcción y Residuos', 3),
        
        # 1.5. Servicios Especiales de Carga
        ('Servicios Especiales de Carga', 'Servicios especiales de carga', 'Transporte de Mercancías', 2),
        ('Transporte de Animales Vivos', 'Transporte de animales vivos', 'Servicios Especiales de Carga', 3),
        ('Portacontenedores Marítimos', 'Portacontenedores marítimos', 'Servicios Especiales de Carga', 3),
        ('Suelo Móvil', 'Transporte con suelo móvil', 'Servicios Especiales de Carga', 3),
        
        # 1.6. Transporte Internacional
        ('Transporte Internacional', 'Transporte internacional', 'Transporte de Mercancías', 2),
        ('Transporte Internacional (Rutas UE)', 'Transporte internacional dentro de la Unión Europea', 'Transporte Internacional', 3),
        ('Transporte Internacional (Rutas Extracomunitarias)', 'Transporte internacional fuera de la UE', 'Transporte Internacional', 3),
        
        # ============================================================
        # 2. TRANSPORTE ESPECIAL Y SERVICIOS DE GRÚA
        # ============================================================
        ('Transporte Especial y Servicios de Grúa', 'Transporte especial y servicios de grúa', None, 1),
        
        # 2.1. Transporte Pesado y Maquinaria
        ('Transporte Pesado y Maquinaria', 'Transporte pesado y maquinaria', 'Transporte Especial y Servicios de Grúa', 2),
        ('Camión Góndola', 'Camión góndola (transporte especial, cargas/maquinaria)', 'Transporte Pesado y Maquinaria', 3),
        
        # 2.2. Servicios de Elevación (Pluma)
        ('Servicios de Elevación (Pluma)', 'Servicios de elevación con pluma', 'Transporte Especial y Servicios de Grúa', 2),
        ('Camión Pluma (Autocargante)', 'Camión pluma autocargante', 'Servicios de Elevación (Pluma)', 3),
        ('Pluma Pequeña', 'Pluma pequeña (< 10 Tm)', 'Camión Pluma (Autocargante)', 4),
        ('Pluma Mediana', 'Pluma mediana (10-25 Tm)', 'Camión Pluma (Autocargante)', 4),
        ('Pluma Grande', 'Pluma grande (> 25 Tm)', 'Camión Pluma (Autocargante)', 4),
        
        # 2.3. Asistencia y Remolque de Vehículos
        ('Asistencia y Remolque de Vehículos', 'Asistencia y remolque de vehículos', 'Transporte Especial y Servicios de Grúa', 2),
        ('Camión Grúa Portacoches', 'Camión grúa portacoches (asistencia ligera/media)', 'Asistencia y Remolque de Vehículos', 3),
        ('Grúa de Arrastre', 'Grúa de arrastre (remolque vehículos pesados)', 'Asistencia y Remolque de Vehículos', 3),
        
        # ============================================================
        # 3. MAQUINARIA DE CONSTRUCCIÓN Y OBRA
        # ============================================================
        ('Maquinaria de Construcción y Obra', 'Maquinaria de construcción y obra', None, 1),
        
        # 3.1. Excavación y Movimiento de Tierras
        ('Excavación y Movimiento de Tierras', 'Excavación y movimiento de tierras', 'Maquinaria de Construcción y Obra', 2),
        ('Mini Excavadora', 'Mini excavadora (orugas / ruedas < 8 Ton)', 'Excavación y Movimiento de Tierras', 3),
        ('Retro Excavadora (Mixta)', 'Retro excavadora mixta', 'Excavación y Movimiento de Tierras', 3),
        ('Giratoria (Excavadora)', 'Excavadora giratoria (orugas / ruedas > 8 Ton)', 'Excavación y Movimiento de Tierras', 3),
        ('Pala Cargadora', 'Pala cargadora (ruedas)', 'Excavación y Movimiento de Tierras', 3),
        ('Mini Cargadora', 'Mini cargadora tipo "Bobcat"', 'Excavación y Movimiento de Tierras', 3),
        ('Motoniveladora', 'Motoniveladora', 'Excavación y Movimiento de Tierras', 3),
        
        # 3.2. Carga y Movimiento de Materiales (Obra)
        ('Carga y Movimiento de Materiales (Obra)', 'Carga y movimiento de materiales en obra', 'Maquinaria de Construcción y Obra', 2),
        ('Dúmper', 'Dúmper (articulado / rígido de obra)', 'Carga y Movimiento de Materiales (Obra)', 3),
        ('Manipulador Telescópico', 'Manipulador telescópico tipo "Manitou"', 'Carga y Movimiento de Materiales (Obra)', 3),
        ('Carretilla Elevadora', 'Carretilla elevadora (toro)', 'Carga y Movimiento de Materiales (Obra)', 3),
        
        # 3.3. Hormigón y Cimentación
        ('Hormigón y Cimentación', 'Hormigón y cimentación', 'Maquinaria de Construcción y Obra', 2),
        ('Camión Bombeo Hormigón', 'Camión bombeo de hormigón', 'Hormigón y Cimentación', 3),
        ('Camión Hormigonera', 'Camión hormigonera', 'Hormigón y Cimentación', 3),
        ('Plantas de Hormigón', 'Plantas de hormigón (móvil / fija)', 'Hormigón y Cimentación', 3),
        
        # 3.4. Compactación y Asfalto
        ('Compactación y Asfalto', 'Compactación y asfalto', 'Maquinaria de Construcción y Obra', 2),
        ('Rodillo Compactador', 'Rodillo compactador (tándem, neumáticos, mixto)', 'Compactación y Asfalto', 3),
        ('Extendedora Asfáltica', 'Extendedora asfáltica', 'Compactación y Asfalto', 3),
        ('Fresadora de Asfalto', 'Fresadora de asfalto', 'Compactación y Asfalto', 3),
        
        # 3.5. Elevación en Obra (PEMP)
        ('Elevación en Obra (PEMP)', 'Elevación en obra (Plataformas Elevadoras Móviles de Personal)', 'Maquinaria de Construcción y Obra', 2),
        ('Plataforma Elevadora (Tijera)', 'Plataforma elevadora tipo tijera', 'Elevación en Obra (PEMP)', 3),
        ('Plataforma Elevadora (Brazo Articulado)', 'Plataforma elevadora de brazo articulado', 'Elevación en Obra (PEMP)', 3),
        ('Plataforma Elevadora sobre Camión', 'Plataforma elevadora montada sobre camión', 'Elevación en Obra (PEMP)', 3),
        
        # ============================================================
        # 4. SECTOR AGRÍCOLA
        # ============================================================
        ('Sector Agrícola', 'Sector agrícola', None, 1),
        
        # 4.1. Maquinaria
        ('Maquinaria', 'Maquinaria agrícola', 'Sector Agrícola', 2),
        ('Tractor', 'Tractor (gomas / orugas)', 'Maquinaria', 3),
        ('Cosechadora', 'Cosechadora (grano, forraje)', 'Maquinaria', 3),
        ('Empacadora / Rotoempacadora', 'Empacadora / rotoempacadora', 'Maquinaria', 3),
        ('Remolque Agrícola', 'Remolque agrícola (baño, plataforma, cisterna purín)', 'Maquinaria', 3),
        
        # 4.2. Servicios (Trabajos Agrícolas)
        ('Servicios (Trabajos Agrícolas)', 'Servicios de trabajos agrícolas', 'Sector Agrícola', 2),
        ('Arado y Preparación de Terreno', 'Arado y preparación de terreno', 'Servicios (Trabajos Agrícolas)', 3),
        ('Siembra y Plantación', 'Siembra y plantación', 'Servicios (Trabajos Agrícolas)', 3),
        ('Tratamientos Fitosanitarios', 'Tratamientos fitosanitarios (pulverización, atomizador)', 'Servicios (Trabajos Agrícolas)', 3),
        ('Cosecha y Recolección', 'Cosecha y recolección', 'Servicios (Trabajos Agrícolas)', 3),
        ('Transporte de Cosecha', 'Transporte de cosecha', 'Servicios (Trabajos Agrícolas)', 3),
        
        # ============================================================
        # 5. MECÁNICA ESPECIALIZADA Y SERVICIOS
        # ============================================================
        ('Mecánica Especializada y Servicios', 'Mecánica especializada y servicios', None, 1),
        
        # 5.1. Mecánica y Asistencia
        ('Mecánica y Asistencia', 'Mecánica y asistencia', 'Mecánica Especializada y Servicios', 2),
        ('Mecánico de Vehículos Pesados (Taller)', 'Mecánico de vehículos pesados en taller', 'Mecánica y Asistencia', 3),
        ('Mecánico de Vehículos Pesados (Asistencia en carretera)', 'Mecánico de vehículos pesados asistencia en carretera', 'Mecánica y Asistencia', 3),
        ('Mecánico de Maquinaria de Obra', 'Mecánico de maquinaria de obra', 'Mecánica y Asistencia', 3),
        ('Mecánico de Maquinaria Agrícola', 'Mecánico de maquinaria agrícola', 'Mecánica y Asistencia', 3),
        ('Servicio Hidráulico', 'Servicio hidráulico (reparación latiguillos)', 'Mecánica y Asistencia', 3),
        ('Servicio de Neumáticos', 'Servicio de neumáticos (vehículo industrial)', 'Mecánica y Asistencia', 3),
        ('Electricista de Vehículo Industrial', 'Electricista de vehículo industrial', 'Mecánica y Asistencia', 3),
        
        # 5.2. Servicios Urbanos e Industriales
        ('Servicios Urbanos e Industriales', 'Servicios urbanos e industriales', 'Mecánica Especializada y Servicios', 2),
        ('Camión Desatoros', 'Camión desatoros (pocería, limpieza alcantarillado)', 'Servicios Urbanos e Industriales', 3),
        ('Barredora Vial', 'Barredora vial', 'Servicios Urbanos e Industriales', 3),
        ('Camión Recogida RSU', 'Camión recogida RSU (basura)', 'Servicios Urbanos e Industriales', 3),
        ('Camión de Riego Asfáltico', 'Camión de riego asfáltico', 'Servicios Urbanos e Industriales', 3),
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


def reverse_load_categorias_v2(apps, schema_editor):
    """Elimina todas las categorías cargadas."""
    Categoria = apps.get_model('db', 'Categoria')
    Categoria.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_load_categorias'),
    ]

    operations = [
        migrations.RunPython(load_categorias_v2, reverse_load_categorias_v2),
    ]
