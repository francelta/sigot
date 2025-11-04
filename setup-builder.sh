#!/bin/bash

# ============================================
# ConnecMaq - Builder.io Integration Setup
# ============================================
# Builder.io es un Visual Headless CMS que permite crear
# el frontend visualmente sin necesidad de carpeta frontend

set -e

echo "============================================"
echo "  ConnecMaq - Builder.io Integration"
echo "============================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[PASO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_title() {
    echo -e "${MAGENTA}$1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -d "backend" ]; then
    print_error "No se encontró el directorio 'backend'. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# 1. Crear carpeta de configuración de Builder.io
print_step "Creando estructura para Builder.io..."

mkdir -p builder-config
mkdir -p builder-config/models
mkdir -p builder-config/templates
mkdir -p builder-config/webhooks

print_success "Estructura de directorios creada"

# 2. Crear archivo de configuración de Builder.io
print_step "Creando archivo de configuración..."

cat > builder-config/builder.config.json << 'EOF'
{
  "name": "ConnecMaq",
  "description": "Plataforma de conexión entre constructores y proveedores de maquinaria pesada",
  "version": "1.0.0",
  "models": [
    {
      "name": "page",
      "kind": "page",
      "description": "Páginas del sitio",
      "fields": [
        {
          "name": "title",
          "type": "string",
          "required": true
        },
        {
          "name": "description",
          "type": "longText"
        }
      ]
    },
    {
      "name": "landing-page",
      "kind": "page",
      "description": "Landing pages de marketing",
      "fields": [
        {
          "name": "title",
          "type": "string",
          "required": true
        },
        {
          "name": "hero_image",
          "type": "file",
          "allowedFileTypes": ["jpeg", "png", "webp"]
        },
        {
          "name": "cta_text",
          "type": "string",
          "defaultValue": "Empezar Ahora"
        },
        {
          "name": "cta_link",
          "type": "string"
        }
      ]
    },
    {
      "name": "blog-post",
      "kind": "data",
      "description": "Posts del blog",
      "fields": [
        {
          "name": "title",
          "type": "string",
          "required": true
        },
        {
          "name": "slug",
          "type": "string",
          "required": true
        },
        {
          "name": "author",
          "type": "string"
        },
        {
          "name": "publishDate",
          "type": "date"
        },
        {
          "name": "content",
          "type": "richText"
        },
        {
          "name": "featured_image",
          "type": "file"
        }
      ]
    }
  ]
}
EOF

print_success "Configuración de modelos creada"

# 3. Crear variables de entorno para Builder.io
print_step "Configurando variables de entorno..."

# Agregar al backend/.env si no existe
if [ -f "backend/.env" ]; then
    if ! grep -q "BUILDER_IO_API_KEY" backend/.env; then
        echo "" >> backend/.env
        echo "# ============================================" >> backend/.env
        echo "# Builder.io Configuration" >> backend/.env
        echo "# ============================================" >> backend/.env
        echo "BUILDER_IO_API_KEY=your-builder-api-key-here" >> backend/.env
        echo "BUILDER_IO_PRIVATE_KEY=your-builder-private-key-here" >> backend/.env
        echo "BUILDER_IO_SPACE_ID=your-space-id" >> backend/.env
        print_success "Variables de Builder.io agregadas a backend/.env"
        print_warning "¡IMPORTANTE! Debes configurar tus keys de Builder.io en backend/.env"
    else
        print_success "Variables de Builder.io ya existen en backend/.env"
    fi
else
    print_warning "No se encontró backend/.env. Créalo primero con ./setup.sh"
fi

# 4. Crear archivo de webhooks para Builder.io
print_step "Creando configuración de webhooks..."

cat > builder-config/webhooks/webhook_handler.py << 'EOF'
"""
Builder.io Webhook Handler
Maneja webhooks de Builder.io para sincronizar contenido
"""
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import hmac
import hashlib
import os

@csrf_exempt
@require_http_methods(["POST"])
def builder_webhook(request):
    """
    Endpoint para recibir webhooks de Builder.io
    URL: /api/builder/webhook/
    """
    
    # Verificar signature
    signature = request.headers.get('X-Builder-Signature')
    private_key = os.getenv('BUILDER_IO_PRIVATE_KEY', '')
    
    if not verify_signature(request.body, signature, private_key):
        return HttpResponseBadRequest('Invalid signature')
    
    try:
        payload = json.loads(request.body)
        event_type = payload.get('type')
        data = payload.get('data')
        
        # Procesar según el tipo de evento
        if event_type == 'publish':
            # Contenido publicado
            print(f"Content published: {data.get('id')}")
            
        elif event_type == 'unpublish':
            # Contenido despublicado
            print(f"Content unpublished: {data.get('id')}")
            
        elif event_type == 'delete':
            # Contenido eliminado
            print(f"Content deleted: {data.get('id')}")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Webhook processed: {event_type}'
        })
        
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def verify_signature(payload, signature, private_key):
    """Verifica la firma del webhook"""
    if not signature or not private_key:
        return False
        
    expected_signature = hmac.new(
        private_key.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)
EOF

print_success "Webhook handler creado"

# 5. Crear vista de integración con Builder.io
print_step "Creando vista de integración Django..."

cat > builder-config/templates/builder_integration.py << 'EOF'
"""
Builder.io Django Integration
Vista para renderizar páginas de Builder.io
"""
from django.shortcuts import render
from django.conf import settings
import requests

def builder_page(request, path=''):
    """
    Renderiza una página de Builder.io
    URL: /<path:path>
    """
    
    api_key = settings.BUILDER_IO_API_KEY
    model = 'page'
    url_path = f"/{path}" if path else "/"
    
    # Obtener contenido de Builder.io
    builder_url = f"https://cdn.builder.io/api/v2/content/{model}"
    params = {
        'apiKey': api_key,
        'url': url_path,
        'cachebust': 'false'
    }
    
    try:
        response = requests.get(builder_url, params=params, timeout=5)
        
        if response.status_code == 200:
            content = response.json()
            
            # Si hay contenido, renderizar
            if content.get('results'):
                return render(request, 'builder_page.html', {
                    'content': content['results'][0],
                    'api_key': api_key
                })
        
        # Si no hay contenido, mostrar 404 o página por defecto
        return render(request, '404.html', status=404)
        
    except requests.RequestException as e:
        print(f"Error fetching Builder.io content: {e}")
        return render(request, '500.html', status=500)
EOF

print_success "Vista de integración creada"

# 6. Crear template HTML para Builder.io
print_step "Creando template HTML..."

cat > builder-config/templates/builder_page.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ content.data.title|default:"ConnecMaq" }}</title>
    
    <!-- Builder.io SDK -->
    <script async src="https://cdn.builder.io/js/webcomponents"></script>
    
    <!-- Styles -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }
    </style>
</head>
<body>
    <!-- Builder.io Content -->
    <builder-component
        model="page"
        api-key="{{ api_key }}"
        content='{{ content|safe }}'
    ></builder-component>
    
    <!-- Script de inicialización -->
    <script>
        // Tracking de analytics
        window.addEventListener('builder:component:load', (event) => {
            console.log('Builder.io content loaded:', event.detail);
        });
    </script>
</body>
</html>
EOF

print_success "Template HTML creado"

# 7. Crear guía de instalación
print_step "Creando documentación..."

cat > builder-config/README.md << 'EOF'
# Builder.io Integration - ConnecMaq

Builder.io es un **Visual Headless CMS** que permite crear el frontend visualmente sin necesidad de código.

## 📋 ¿Qué es Builder.io?

Builder.io permite a diseñadores y marketers crear páginas web visualmente usando un editor drag-and-drop, mientras los desarrolladores controlan los componentes y la lógica de negocio.

**Ventajas:**
- ✅ No requiere carpeta `frontend/`
- ✅ Editor visual drag-and-drop
- ✅ Integración directa con Django backend
- ✅ CDN global de alto rendimiento
- ✅ A/B testing integrado
- ✅ Personalización sin código

## 🚀 Setup Completo

### 1. Crear Cuenta en Builder.io

```bash
1. Ve a https://builder.io
2. Crea una cuenta gratuita
3. Crea un nuevo "Space" para ConnecMaq
```

### 2. Obtener API Keys

```bash
1. En Builder.io, ve a Settings → API Keys
2. Copia tu Public API Key
3. Copia tu Private Key (para webhooks)
4. Copia tu Space ID
```

### 3. Configurar Backend

Edita `backend/.env`:

```env
BUILDER_IO_API_KEY=tu-public-api-key
BUILDER_IO_PRIVATE_KEY=tu-private-key
BUILDER_IO_SPACE_ID=tu-space-id
```

### 4. Agregar URLs de Django

En `backend/config/urls.py`:

```python
from builder_config.webhooks.webhook_handler import builder_webhook
from builder_config.templates.builder_integration import builder_page

urlpatterns = [
    # ... otras URLs
    
    # Builder.io webhook
    path('api/builder/webhook/', builder_webhook, name='builder-webhook'),
    
    # Builder.io pages (debe ir al final)
    path('<path:path>', builder_page, name='builder-page'),
    path('', builder_page, name='builder-home'),
]
```

### 5. Instalar Dependencias Python

```bash
cd backend
source venv/bin/activate
pip install requests
```

### 6. Configurar Webhook en Builder.io

```bash
1. En Builder.io, ve a Settings → Webhooks
2. Agrega nuevo webhook:
   URL: https://tu-dominio.com/api/builder/webhook/
   Events: publish, unpublish, delete
3. Copia el Secret y agrégalo a BUILDER_IO_PRIVATE_KEY
```

## 🎨 Crear Tu Primera Página

### En Builder.io:

1. **Crear Modelo (si no existe):**
   - Ve a Models
   - Click "New Model"
   - Nombre: "page"
   - Kind: "Page"

2. **Crear Página:**
   - Ve a Content
   - Click "New"
   - Selecciona modelo "page"
   - URL: `/` (home) o `/about`, etc.
   - Usa el editor visual para diseñar

3. **Publicar:**
   - Click "Publish"
   - La página estará disponible inmediatamente

### En tu Backend Django:

La integración está lista. Las páginas se renderizan automáticamente en las URLs que configures en Builder.io.

## 📊 Modelos Pre-configurados

### 1. Page (Página básica)
- URL: Cualquier ruta
- Uso: Páginas estáticas (Home, About, Contact)

### 2. Landing Page
- URL: /landing/*
- Uso: Páginas de marketing con CTAs
- Campos: Hero Image, CTA Text, CTA Link

### 3. Blog Post
- URL: /blog/*
- Uso: Posts de blog
- Campos: Title, Slug, Author, Content, Featured Image

## 🔌 Integración con API Django

### Pasar Datos del Backend a Builder.io:

```python
def builder_page_with_data(request, path=''):
    # Obtener datos de tu backend
    providers = Provider.objects.filter(available_within_48h=True)[:5]
    
    # Renderizar con datos
    return render(request, 'builder_page.html', {
        'content': builder_content,
        'api_key': settings.BUILDER_IO_API_KEY,
        'providers': providers,  # Datos dinámicos
    })
```

En Builder.io, usa "Custom Code" para acceder a los datos.

## 🧪 Testing Local

1. **Ejecuta el backend:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Accede a:**
   ```
   http://localhost:8000/
   ```

3. **Preview en Builder.io:**
   - En el editor, configura Preview URL:
   - `http://localhost:8000/`

## 📱 Ejemplo de Uso

### Home Page:
```
URL en Builder.io: /
Renderiza en: http://tu-dominio.com/
```

### Landing Page para Constructores:
```
URL en Builder.io: /constructores
Renderiza en: http://tu-dominio.com/constructores
```

### Blog:
```
URL en Builder.io: /blog/mi-post
Renderiza en: http://tu-dominio.com/blog/mi-post
```

## 🎯 Ventajas para ConnecMaq

1. **Marketing Ágil:**
   - El equipo de marketing puede crear landing pages sin esperar a desarrollo
   
2. **A/B Testing:**
   - Prueba diferentes versiones de páginas

3. **Personalización:**
   - Muestra contenido diferente según tipo de usuario (constructor vs proveedor)

4. **Performance:**
   - CDN global = carga rápida en todo el mundo

5. **SEO:**
   - Server-side rendering automático
   - Meta tags configurables

## 📚 Recursos

- [Builder.io Docs](https://www.builder.io/c/docs/intro)
- [Django Integration](https://www.builder.io/c/docs/integrating-builder-pages)
- [Visual Editor](https://www.builder.io/c/docs/guides)
- [Custom Components](https://www.builder.io/c/docs/custom-components-setup)

## 💡 Tips

- Usa "Symbols" en Builder.io para componentes reutilizables (header, footer)
- Configura "Targeting" para mostrar contenido específico por audiencia
- Usa "Scheduling" para publicar contenido en fechas específicas
- Integra con Analytics (Google Analytics, Segment, etc.)

## 🔒 Seguridad

- Nunca expongas tu Private Key en el frontend
- Usa el Private Key solo para webhooks en el backend
- Configura CORS correctamente en Django para Builder.io

---

**¿Necesitas ayuda?**
- Builder.io Support: https://www.builder.io/c/support
- ConnecMaq Docs: Ver otros archivos .md en el proyecto
EOF

print_success "Documentación creada"

# 8. Crear archivo de ejemplo de configuración Django
print_step "Creando ejemplo de configuración Django..."

cat > builder-config/django_settings_example.py << 'EOF'
"""
Ejemplo de configuración de Django para Builder.io
Agrega estas configuraciones a tu backend/config/settings.py
"""

# Builder.io Configuration
BUILDER_IO_API_KEY = os.getenv('BUILDER_IO_API_KEY', '')
BUILDER_IO_PRIVATE_KEY = os.getenv('BUILDER_IO_PRIVATE_KEY', '')
BUILDER_IO_SPACE_ID = os.getenv('BUILDER_IO_SPACE_ID', '')

# Agregar a INSTALLED_APPS (opcional, si creas una app de builder)
# INSTALLED_APPS = [
#     ...
#     'builder',
# ]

# Templates (si usas templates de Django)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'builder-config' / 'templates',  # Agregar esta línea
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
EOF

print_success "Ejemplo de configuración creado"

# 9. Resumen final
echo ""
echo "============================================"
echo -e "${GREEN}  ✓ Builder.io Setup Completado${NC}"
echo "============================================"
echo ""
print_title "📦 Archivos Creados:"
echo "  ✓ builder-config/"
echo "    ├── builder.config.json       (Modelos de contenido)"
echo "    ├── README.md                 (Documentación completa)"
echo "    ├── django_settings_example.py"
echo "    ├── webhooks/"
echo "    │   └── webhook_handler.py    (Handler de webhooks)"
echo "    └── templates/"
echo "        ├── builder_integration.py (Vista Django)"
echo "        └── builder_page.html      (Template HTML)"
echo ""
print_title "⚡ SIGUIENTES PASOS:"
echo ""
echo "1. 🌐 Crear Cuenta en Builder.io"
echo "   → https://builder.io"
echo "   → Crea un Space para ConnecMaq"
echo ""
echo "2. 🔑 Obtener API Keys"
echo "   → Settings → API Keys"
echo "   → Copia Public API Key, Private Key y Space ID"
echo ""
echo "3. ⚙️  Configurar Backend"
echo "   → Edita backend/.env"
echo "   → Agrega tus keys de Builder.io"
echo ""
echo "4. 📝 Integrar con Django"
echo "   → Sigue las instrucciones en builder-config/README.md"
echo "   → Agrega URLs a backend/config/urls.py"
echo ""
echo "5. 🎨 Crear Primera Página"
echo "   → En Builder.io: Content → New → Page"
echo "   → URL: / (home)"
echo "   → Diseña visualmente"
echo "   → Publish"
echo ""
print_title "📚 Documentación:"
echo "  → builder-config/README.md (Guía completa)"
echo "  → https://www.builder.io/c/docs"
echo ""
print_title "💡 Ventajas de Builder.io:"
echo "  ✓ No necesitas carpeta frontend/"
echo "  ✓ Editor visual drag-and-drop"
echo "  ✓ CDN global de alto rendimiento"
echo "  ✓ A/B testing integrado"
echo "  ✓ Marketing puede crear páginas sin desarrollo"
echo ""
echo "============================================"
print_success "¡Builder.io listo para usar!"
echo "============================================"
