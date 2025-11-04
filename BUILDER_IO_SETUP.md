# 🎨 Builder.io Setup - ConnecMaq

## ✅ Setup Completado

Se ha creado la integración completa con **Builder.io** como Visual Headless CMS para ConnecMaq.

---

## 🤔 ¿Qué es Builder.io?

**Builder.io** es un **Visual Headless CMS** que permite crear el frontend de tu aplicación web visualmente, sin necesidad de código.

### ❌ NO es un framework frontend

Builder.io **NO** requiere:
- ❌ Carpeta `frontend/`
- ❌ Proyecto Vue/React/Angular separado
- ❌ npm install de dependencias frontend
- ❌ Compilar o hacer build

### ✅ Es una plataforma visual

Builder.io **ES**:
- ✅ Un editor drag-and-drop en la nube
- ✅ Un CDN global que sirve tu contenido
- ✅ Una plataforma donde diseñadores crean páginas sin código
- ✅ Un CMS que se integra directamente con tu backend Django

---

## 🎯 ¿Cómo Funciona?

```
┌──────────────────────────────────────────────┐
│ 1. Creas páginas en Builder.io              │
│    (Editor visual en el navegador)           │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ 2. Publicas el contenido                    │
│    (Se almacena en Builder.io CDN)           │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ 3. Tu backend Django renderiza la página    │
│    (Obtiene contenido del CDN de Builder.io)│
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│ 4. Usuario ve la página                     │
│    (HTML + CSS + JS desde Builder.io)        │
└──────────────────────────────────────────────┘
```

---

## 📦 Archivos Creados

```
sigot/
├── setup-builder.sh          # Script de setup Unix/Mac
├── setup-builder.bat         # Script de setup Windows
├── Makefile                  # Comandos make actualizados
└── builder-config/           # Se crea al ejecutar setup-builder.sh
    ├── README.md             # Documentación completa
    ├── builder.config.json   # Modelos de contenido
    ├── django_settings_example.py
    ├── webhooks/
    │   └── webhook_handler.py
    └── templates/
        ├── builder_integration.py
        └── builder_page.html
```

---

## 🚀 Instalación

### Opción 1: Script Automático

**Unix/Mac/Linux:**
```bash
./setup-builder.sh
```

**Windows:**
```batch
setup-builder.bat
```

### Opción 2: Makefile

```bash
make setup-builder
```

---

## 📝 Pasos Después del Setup

### 1. Crear Cuenta en Builder.io

```bash
1. Ve a https://builder.io
2. Crea una cuenta gratuita
3. Crea un nuevo "Space" llamado "ConnecMaq"
```

### 2. Obtener API Keys

```bash
1. En Builder.io, ve a: Account → Settings → API Keys
2. Copia:
   - Public API Key (para frontend)
   - Private Key (para webhooks)
   - Space ID (opcional)
```

### 3. Configurar Backend

Edita `backend/.env`:

```env
# Builder.io Configuration
BUILDER_IO_API_KEY=tu-public-api-key-aqui
BUILDER_IO_PRIVATE_KEY=tu-private-key-aqui
BUILDER_IO_SPACE_ID=tu-space-id-aqui
```

### 4. Agregar URLs a Django

Edita `backend/config/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

# Importar las vistas de Builder.io (agregar después de ejecutar setup)
# from builder_config.webhooks.webhook_handler import builder_webhook
# from builder_config.templates.builder_integration import builder_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Builder.io webhook (descomenta después de ejecutar setup-builder.sh)
    # path('api/builder/webhook/', builder_webhook, name='builder-webhook'),
    
    # Builder.io pages - DEBE IR AL FINAL (descomenta después de ejecutar setup-builder.sh)
    # path('<path:path>', builder_page, name='builder-page'),
    # path('', builder_page, name='builder-home'),
]
```

### 5. Instalar Dependencia Python

```bash
cd backend
source venv/bin/activate
pip install requests
```

O con make:

```bash
make builder-install-deps
```

---

## 🎨 Crear Tu Primera Página

### En Builder.io (navegador):

1. **Ir a Models:**
   - Sidebar → Models
   - Verifica que exista el modelo "page"
   - Si no existe, créalo:
     - Click "New Model"
     - Name: `page`
     - Kind: "Page"
     - Save

2. **Crear Contenido:**
   - Sidebar → Content
   - Click "+ New"
   - Select model: "page"
   - Enter URL: `/` (para home page)

3. **Diseñar:**
   - Usa el editor visual drag-and-drop
   - Agrega bloques (Text, Image, Button, etc.)
   - Personaliza colores, fuentes, espaciado

4. **Publicar:**
   - Click "Publish" (arriba a la derecha)
   - La página estará disponible inmediatamente

### En tu Backend Django:

1. **Ejecutar servidor:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Visitar:**
   ```
   http://localhost:8000/
   ```

3. **Ver tu página:**
   - Deberías ver el contenido que creaste en Builder.io
   - Carga instantánea desde CDN

---

## 📊 Modelos Pre-configurados

### 1. Page (Página Básica)

```json
{
  "name": "page",
  "kind": "page",
  "description": "Páginas del sitio",
  "fields": ["title", "description"]
}
```

**Uso:** Páginas estáticas (Home, About, Contact, etc.)

**URLs:** Cualquier ruta (`/`, `/about`, `/contact`)

### 2. Landing Page

```json
{
  "name": "landing-page",
  "kind": "page",
  "description": "Landing pages de marketing",
  "fields": ["title", "hero_image", "cta_text", "cta_link"]
}
```

**Uso:** Páginas de marketing con CTAs

**URLs:** `/landing/constructores`, `/landing/proveedores`

### 3. Blog Post

```json
{
  "name": "blog-post",
  "kind": "data",
  "description": "Posts del blog",
  "fields": ["title", "slug", "author", "publishDate", "content", "featured_image"]
}
```

**Uso:** Blog de ConnecMaq

**URLs:** `/blog/[slug]`

---

## 🔌 Integración con API Django

### Pasar Datos del Backend a Builder.io

Puedes inyectar datos de tu backend Django en las páginas de Builder.io:

```python
# En builder_integration.py (modificado)

def builder_page_with_data(request, path=''):
    # Obtener contenido de Builder.io
    builder_content = fetch_builder_content(path)
    
    # Obtener datos de tu backend
    providers = ProviderProfile.objects.filter(
        available_within_48h=True
    )[:5]
    
    machines = Machine.objects.filter(
        is_available=True
    )[:10]
    
    # Renderizar con datos combinados
    return render(request, 'builder_page.html', {
        'content': builder_content,
        'api_key': settings.BUILDER_IO_API_KEY,
        'providers': providers,
        'machines': machines,
    })
```

Luego en Builder.io, usa "Custom Code" para acceder a estos datos.

---

## 💡 Casos de Uso para ConnecMaq

### 1. Landing Pages de Marketing

**Escenario:** El equipo de marketing quiere crear una landing page para captar constructores.

**Con Builder.io:**
- Marketing crea la página en Builder.io (sin código)
- Agrega formularios, CTAs, imágenes
- Publica inmediatamente
- Sin esperar a desarrollo

**Sin Builder.io:**
- Requiere desarrollador
- Crear componentes Vue
- Deploy
- Proceso lento

### 2. Páginas Estáticas

**Home, About, Contact, Terms, Privacy**

- Crea una vez en Builder.io
- Modifica cuando quieras sin deployment
- A/B testing automático

### 3. Blog de Contenido

**Para SEO y atracción de clientes**

- Marketing publica artículos
- Sin tocar código
- SEO optimizado automáticamente

### 4. Páginas Personalizadas por Audiencia

**Mostrar diferente contenido a constructores vs proveedores**

- Builder.io tiene "Targeting"
- Muestra variaciones según usuario
- Sin código adicional

---

## 🎯 Ventajas para ConnecMaq

| Ventaja | Descripción |
|---------|-------------|
| 🚀 **Velocidad** | Marketing crea páginas en minutos, no días |
| 💰 **Costo** | Menos tiempo de desarrollo = menos costo |
| 🎨 **Flexibilidad** | Cambios sin redeploy |
| 📊 **A/B Testing** | Prueba variaciones sin código |
| 🌍 **Performance** | CDN global = carga rápida mundial |
| 📱 **Responsive** | Automático para móviles |
| 🔍 **SEO** | Server-side rendering incluido |
| 🎯 **Targeting** | Contenido personalizado por audiencia |

---

## 📚 Comandos Make Disponibles

```bash
make setup-builder      # Ejecutar setup completo
make builder-docs       # Ver documentación
make builder-install-deps  # Instalar dependencias Python
```

---

## 🧪 Testing Local

### 1. Configurar Preview URL en Builder.io

En el editor de Builder.io:

1. Click en Settings (⚙️)
2. Preview URLs
3. Agrega: `http://localhost:8000`

### 2. Ejecutar Backend

```bash
cd backend
python manage.py runserver
```

### 3. Preview en Tiempo Real

- Mientras editas en Builder.io
- Click "Preview"
- Ve los cambios en `localhost:8000`

---

## 🔐 Seguridad

### ✅ Hacer

- ✅ Usar Public API Key en templates HTML
- ✅ Usar Private Key solo en webhooks (backend)
- ✅ Configurar CORS en Django para Builder.io CDN
- ✅ Validar webhooks con signature

### ❌ NO Hacer

- ❌ Exponer Private Key en frontend
- ❌ Hardcodear API keys en código (usar .env)
- ❌ Deshabilitar CSRF para webhooks sin validación

---

## 📖 Recursos

### Builder.io

- **Docs:** https://www.builder.io/c/docs/intro
- **Django Integration:** https://www.builder.io/c/docs/integrating-builder-pages
- **Visual Editor:** https://www.builder.io/c/docs/guides
- **Custom Components:** https://www.builder.io/c/docs/custom-components-setup

### ConnecMaq

- **README Principal:** [README.md](README.md)
- **Instalación:** [INSTALL.md](INSTALL.md)
- **Comandos:** [COMANDOS.md](COMANDOS.md)
- **Configuración Builder.io:** `builder-config/README.md` (se crea al ejecutar setup)

---

## ❓ FAQ

### ¿Por qué Builder.io en vez de Vue.js tradicional?

**Builder.io:**
- ✅ Marketing puede crear páginas sin desarrollo
- ✅ Cambios instantáneos sin deployment
- ✅ A/B testing incluido
- ✅ CDN global incluido

**Vue.js Tradicional:**
- ❌ Requiere desarrollador para cada cambio
- ❌ Requiere deployment
- ❌ A/B testing manual
- ❌ CDN requiere configuración

### ¿Puedo usar ambos?

¡Sí! Puedes usar:
- **Builder.io** para páginas de marketing, landing pages, blog
- **Vue.js** para la aplicación web (dashboard, forms complejos)

### ¿Cuánto cuesta?

- **Free:** Hasta 1,000 visitas/mes
- **Paid:** Desde $29/mes
- **Enterprise:** Custom pricing

Para ConnecMaq en fase inicial, el plan Free es suficiente.

### ¿Necesito saber programar para usar Builder.io?

**No.** Builder.io está diseñado para diseñadores y marketers sin conocimientos de programación.

Sin embargo, desarrolladores pueden crear componentes personalizados para el equipo.

---

## 🎊 Resumen

✅ **Setup Completado:**
- Scripts de instalación creados
- Estructura de archivos lista
- Documentación completa
- Integración con Django configurada

🚀 **Siguientes Pasos:**
1. Crear cuenta en Builder.io
2. Obtener API keys
3. Configurar backend/.env
4. Crear primera página
5. ¡Empezar a usar!

💡 **Ventaja Principal:**
Marketing puede crear y modificar páginas sin esperar a desarrollo.

---

**¿Listo para empezar?**

```bash
./setup-builder.sh
```

¡Y crea tu primera página en Builder.io! 🎨

