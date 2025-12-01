# Migration to load initial categories

from django.db import migrations


def load_categorias(apps, schema_editor):
    Categoria = apps.get_model('db', 'Categoria')
    
    # Categorías principales
    categorias_principales = [
        {'nombre': 'Transporte de Mercancías', 'descripcion': 'Transporte general de mercancías y carga'},
        {'nombre': 'Transporte de Maquinaria', 'descripcion': 'Transporte de maquinaria pesada y equipos industriales'},
        {'nombre': 'Transporte Especial', 'descripcion': 'Transporte de cargas especiales y sobredimensionadas'},
        {'nombre': 'Grúas y Elevación', 'descripcion': 'Servicios de grúas y equipos de elevación'},
    ]
    
    padres = {}
    for cat_data in categorias_principales:
        cat, _ = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion'], 'parent': None}
        )
        padres[cat_data['nombre']] = cat
    
    # Subcategorías
    subcategorias = [
        # Mercancías
        {'nombre': 'Carga General', 'descripcion': 'Transporte de carga general paletizada', 'parent': 'Transporte de Mercancías'},
        {'nombre': 'Carga Refrigerada', 'descripcion': 'Transporte con temperatura controlada', 'parent': 'Transporte de Mercancías'},
        {'nombre': 'Mercancías Peligrosas', 'descripcion': 'Transporte ADR de mercancías peligrosas', 'parent': 'Transporte de Mercancías'},
        {'nombre': 'Contenedores', 'descripcion': 'Transporte de contenedores marítimos', 'parent': 'Transporte de Mercancías'},
        
        # Maquinaria
        {'nombre': 'Excavadoras', 'descripcion': 'Transporte de excavadoras y retroexcavadoras', 'parent': 'Transporte de Maquinaria'},
        {'nombre': 'Bulldozers', 'descripcion': 'Transporte de bulldozers y topadoras', 'parent': 'Transporte de Maquinaria'},
        {'nombre': 'Tractores', 'descripcion': 'Transporte de tractores agrícolas', 'parent': 'Transporte de Maquinaria'},
        {'nombre': 'Maquinaria Agrícola', 'descripcion': 'Cosechadoras, sembradoras y equipos agrícolas', 'parent': 'Transporte de Maquinaria'},
        {'nombre': 'Carretillas Elevadoras', 'descripcion': 'Transporte de carretillas y montacargas', 'parent': 'Transporte de Maquinaria'},
        
        # Especial
        {'nombre': 'Cargas Sobredimensionadas', 'descripcion': 'Transporte de cargas que exceden dimensiones normales', 'parent': 'Transporte Especial'},
        {'nombre': 'Cargas Pesadas', 'descripcion': 'Transporte de cargas de gran tonelaje', 'parent': 'Transporte Especial'},
        {'nombre': 'Vehículos', 'descripcion': 'Transporte de vehículos y automóviles', 'parent': 'Transporte Especial'},
        {'nombre': 'Embarcaciones', 'descripcion': 'Transporte de barcos y embarcaciones', 'parent': 'Transporte Especial'},
        
        # Grúas
        {'nombre': 'Grúas Móviles', 'descripcion': 'Servicio de grúas móviles sobre ruedas', 'parent': 'Grúas y Elevación'},
        {'nombre': 'Grúas Torre', 'descripcion': 'Montaje y desmontaje de grúas torre', 'parent': 'Grúas y Elevación'},
        {'nombre': 'Plataformas Elevadoras', 'descripcion': 'Servicio de plataformas de elevación', 'parent': 'Grúas y Elevación'},
    ]
    
    for subcat_data in subcategorias:
        parent = padres.get(subcat_data['parent'])
        Categoria.objects.get_or_create(
            nombre=subcat_data['nombre'],
            defaults={'descripcion': subcat_data['descripcion'], 'parent': parent}
        )


def reverse_load_categorias(apps, schema_editor):
    Categoria = apps.get_model('db', 'Categoria')
    Categoria.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_categorias, reverse_load_categorias),
    ]


