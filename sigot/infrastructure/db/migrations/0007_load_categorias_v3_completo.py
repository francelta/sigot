# Generated migration to load complete category taxonomy v3.0
# Based on user requirements

from django.db import migrations


def load_categorias_v3(apps, schema_editor):
    """
    Carga la taxonomía completa de categorías v3.0 según especificaciones del usuario.
    """
    Categoria = apps.get_model('db', 'Categoria')
    
    # Estructura completa de categorías
    categorias_data = {
        'Transporte de Mercancías': {
            'Carga General (Seca)': {
                'Transporte Ligero (Furgoneta / Carrozado)': None,
                'Camión Paquetero': None,
                'Camión <= 3500kg (Chasis-cabina, Plataforma, etc.)': None,
                'Camión Rígido (2 y 3 ejes > 3500kg)': None,
                'Camión Articulado (Tráiler)': {
                    'Tráiler Lona (Tauliner)': None,
                    'Tráiler Plataforma (Plana)': None,
                    'Tráiler Portabobinas': None,
                },
            },
            'Temperatura Controlada': {
                'Camión Frigorífico (Refrigerado / Congelado)': None,
                'Camión Isotermo (Sin equipo de frío)': None,
            },
            'Cisternas (Líquidos, Polvos, Gases)': {
                'Camión Cubas (Término genérico, p.ej. agua)': None,
                'Cisterna de Agua (Riego, Potable, No potable)': None,
                'Cisterna de Combustible / ADR': None,
                'Cisterna Alimentaria (Leche, Vino, Aceite)': None,
                'Cisterna Pulverulentos (Cemento, Harina, Pienso)': None,
                'Cisterna de Gases (GLP, GNL, Criogénicos)': None,
            },
            'Áridos, Construcción y Residuos': {
                'Camión Basculante (Volquete) (2/3 ejes)': None,
                'Camión Portacontenedores (Gancho / Multilift)': None,
                'Bañera (Semirremolque basculante)': None,
            },
            'Servicios Especiales de Carga': {
                'Transporte de Animales Vivos': None,
                'Portacontenedores Marítimos': None,
                'Suelo Móvil': None,
            },
            'Transporte Internacional': {
                'Transporte Internacional (Rutas UE)': None,
                'Transporte Internacional (Rutas Extracomunitarias)': None,
            },
        },
        'Transporte Especial y Servicios de Grúa': {
            'Transporte Pesado y Maquinaria': {
                'Camión Góndola (Transporte Especial, Cargas/Maquinaria)': None,
            },
            'Servicios de Elevación (Pluma)': {
                'Camión Pluma (Autocargante)': {
                    'Pluma Pequeña (< 10 Tm)': None,
                    'Pluma Mediana (10-25 Tm)': None,
                    'Pluma Grande (> 25 Tm)': None,
                },
            },
            'Asistencia y Remolque de Vehículos': {
                'Camión Grúa Portacoches (Asistencia ligera/media)': None,
                'Grúa de Arrastre (Remolque vehículos pesados)': None,
            },
        },
        'Maquinaria de Construcción y Obra': {
            'Excavación y Movimiento de Tierras': {
                'Mini Excavadora (Orugas / Ruedas < 8 Ton)': None,
                'Retro Excavadora (Mixta)': None,
                'Giratoria (Excavadora) (Orugas / Ruedas > 8 Ton)': None,
                'Pala Cargadora (Ruedas)': None,
                'Mini Cargadora (Tipo "Bobcat")': None,
                'Motoniveladora': None,
            },
            'Carga y Movimiento de Materiales (Obra)': {
                'Dúmper (Articulado / Rígido de obra)': None,
                'Manipulador Telescópico (Tipo "Manitou")': None,
                'Carretilla Elevadora (Toro)': None,
            },
            'Hormigón y Cimentación': {
                'Camión Bombeo Hormigón': None,
                'Camión Hormigonera': None,
                'Plantas de Hormigón (Móvil / Fija)': None,
            },
            'Compactación y Asfalto': {
                'Rodillo Compactador (Tándem, Neumáticos, Mixto)': None,
                'Extendedora Asfáltica': None,
                'Fresadora de Asfalto': None,
            },
            'Elevación en Obra (PEMP)': {
                'Plataforma Elevadora (Tijera)': None,
                'Plataforma Elevadora (Brazo Articulado)': None,
                'Plataforma Elevadora sobre Camión': None,
            },
        },
        'Sector Agrícola': {
            'Maquinaria': {
                'Tractor (Gomas / Orugas)': None,
                'Cosechadora (Grano, Forraje)': None,
                'Empacadora / Rotoempacadora': None,
                'Remolque Agrícola (Baño, Plataforma, Cisterna Purín)': None,
            },
            'Servicios (Trabajos Agrícolas)': {
                'Arado y Preparación de Terreno': None,
                'Siembra y Plantación': None,
                'Tratamientos Fitosanitarios (Pulverización, Atomizador)': None,
                'Cosecha y Recolección': None,
                'Transporte de Cosecha': None,
            },
        },
        'Mecánica Especializada y Servicios': {
            'Mecánica y Asistencia': {
                'Mecánico de Vehículos Pesados (Taller)': None,
                'Mecánico de Vehículos Pesados (Asistencia en carretera)': None,
                'Mecánico de Maquinaria de Obra': None,
                'Mecánico de Maquinaria Agrícola': None,
                'Servicio Hidráulico (Reparación latiguillos)': None,
                'Servicio de Neumáticos (Vehículo industrial)': None,
                'Electricista de Vehículo Industrial': None,
            },
            'Servicios Urbanos e Industriales': {
                'Camión Desatoros (Pocería, Limpieza alcantarillado)': None,
                'Barredora Vial': None,
                'Camión Recogida RSU (Basura)': None,
                'Camión de Riego Asfáltico': None,
            },
        },
    }
    
    def create_categoria_recursive(nombre, parent=None, children=None):
        """Crea una categoría y recursivamente sus hijos."""
        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={
                'parent': parent,
                'descripcion': f'Categoría: {nombre}'
            }
        )
        
        if children:
            for child_nombre, grand_children in children.items():
                create_categoria_recursive(child_nombre, parent=categoria, children=grand_children)
    
    # Crear todas las categorías recursivamente
    for root_nombre, children in categorias_data.items():
        create_categoria_recursive(root_nombre, parent=None, children=children)


def reverse_load_categorias_v3(apps, schema_editor):
    """
    Elimina las categorías creadas (opcional, para rollback).
    """
    Categoria = apps.get_model('db', 'Categoria')
    # Eliminar todas las categorías (o solo las nuevas si quieres ser más específico)
    Categoria.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_transportistacategoria_caracteristicas_and_more'),
    ]

    operations = [
        migrations.RunPython(load_categorias_v3, reverse_load_categorias_v3),
    ]


