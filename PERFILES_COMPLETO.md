# 📝 Sistema de Perfiles Completo - ConnecMaq

## ✅ Funcionalidad Implementada

Se ha implementado un sistema completo de creación y edición de perfiles para **Constructores** y **Proveedores**, con interfaces visuales modernas y validación completa.

---

## 📂 Archivos Creados/Modificados

### Vistas Nuevas

1. **`/frontend/src/views/constructor/CreateProfile.vue`**
   - Formulario para crear perfil de constructor
   - Campos: Empresa, teléfono, dirección, ciudad, región
   - Validación de campos requeridos

2. **`/frontend/src/views/provider/CreateProfile.vue`**
   - Formulario para crear perfil de proveedor
   - Campos: Empresa, descripción, logo, teléfono, web, dirección, ciudad, región
   - Toggle "Disponible en < 48h"
   - Upload de logo con preview
   - Validación de tamaño (máx 2MB)

3. **`/frontend/src/views/common/EditProfile.vue`**
   - Vista universal de edición
   - Detecta automáticamente si es constructor o proveedor
   - Muestra formulario apropiado según tipo de usuario
   - Permite actualizar todos los campos
   - Para proveedores: cambio de logo opcional

### Vistas Mejoradas

4. **`/frontend/src/views/common/Profile.vue`** (MEJORADA)
   - Vista completa del perfil
   - Información de usuario
   - Información del perfil (constructor o proveedor)
   - Estadísticas (para proveedores)
   - Botón "Editar Perfil"
   - Enlaces para crear perfil si no existe

5. **`/frontend/src/views/constructor/Dashboard.vue`** (MEJORADA)
   - Alerta visual si no tiene perfil
   - Botón directo a "Crear Perfil"

6. **`/frontend/src/views/provider/Dashboard.vue`** (MEJORADA)
   - Alerta visual si no tiene perfil
   - Botón directo a "Crear Perfil"
   - Toggle 48h solo visible si tiene perfil

### Rutas Agregadas

7. **`/frontend/src/router/index.js`** (ACTUALIZADO)
   - `/constructor/create-profile` → Crear perfil constructor
   - `/provider/create-profile` → Crear perfil proveedor
   - `/edit-profile` → Editar perfil (universal)

---

## 🎨 Características del Sistema de Perfiles

### Para Constructores

**Campos del Perfil:**
- ✅ Nombre de la empresa (requerido)
- ✅ Teléfono
- ✅ Dirección
- ✅ Ciudad (requerido)
- ✅ Región (requerido)
- ✅ País (default: Chile)

**Flujo de Usuario:**
1. Usuario se registra como Constructor
2. Ve alerta en Dashboard: "Completa tu perfil"
3. Click en "Crear Perfil Ahora"
4. Rellena formulario
5. Submit → Perfil creado ✅
6. Redirección automática al Dashboard

### Para Proveedores

**Campos del Perfil:**
- ✅ Nombre de la empresa (requerido)
- ✅ Descripción
- ✅ Logo (upload de imagen, máx 2MB)
- ✅ Teléfono (requerido)
- ✅ Sitio web
- ✅ Dirección
- ✅ Ciudad (requerido)
- ✅ Región (requerido)
- ✅ País (default: Chile)
- ✅ **Disponible en < 48h** (toggle, default: true)

**Flujo de Usuario:**
1. Usuario se registra como Proveedor
2. Ve alerta en Dashboard: "Completa tu perfil de proveedor"
3. Click en "Crear Perfil Ahora"
4. Rellena formulario
5. Opcionalmente sube logo (ve preview antes de submit)
6. Activa/desactiva "Disponible en < 48h"
7. Submit → Perfil creado ✅
8. Redirección automática al Dashboard

---

## 🎯 Características Destacadas

### 1. Vista de Perfil Mejorada

**Constructor:**
```
┌─────────────────────────────────────┐
│ Mi Perfil          [Editar Perfil]  │
├─────────────────────────────────────┤
│ Información de Usuario              │
│ - Email                             │
│ - Username                          │
│ - Tipo: 👷 Constructor              │
├─────────────────────────────────────┤
│ Perfil de Constructor               │
│ - Empresa                           │
│ - Teléfono                          │
│ - Ciudad / Región                   │
│ - Dirección                         │
└─────────────────────────────────────┘
```

**Proveedor:**
```
┌─────────────────────────────────────┐
│ Mi Perfil          [Editar Perfil]  │
├─────────────────────────────────────┤
│ Perfil de Proveedor                 │
│ [LOGO]                              │
│ Empresa: Maquinarias del Sur        │
│ Estado: [Active] 🟢                 │
│ Descripción...                      │
│ Teléfono / Web                      │
│ Ciudad / Región                     │
│                                     │
│ ⚡ Disponible en < 48h              │
│ (Apareces en búsquedas rápidas)     │
├─────────────────────────────────────┤
│ Estadísticas                        │
│ [5 Maquinarias] [0 Servicios]      │
│ [0 Chats] [0 Valoraciones]         │
└─────────────────────────────────────┘
```

### 2. Alertas en Dashboards

Si el usuario **NO** tiene perfil:

```
┌─────────────────────────────────────────┐
│ ⚠️  Completa tu perfil                  │
│                                         │
│ Para obtener todos los beneficios       │
│ de la plataforma...                     │
│                                         │
│ [Crear Perfil Ahora]                    │
└─────────────────────────────────────────┘
```

### 3. Upload de Logo con Preview

Para proveedores:
```javascript
// Validaciones:
- Tamaño máximo: 2MB
- Tipo: Solo imágenes (image/*)
- Preview en tiempo real antes de submit
- Imagen opcional al editar (mantiene la anterior)
```

### 4. Toggle "Disponible en < 48h"

```
┌──────────────────────────────────────┐
│ ⚡ Disponible en menos de 48 horas   │
│                                      │
│ Activa esto si puedes confirmar     │
│ servicios en menos de 48 horas.      │
│ Aparecerás en búsquedas prioritarias │
└──────────────────────────────────────┘
```

---

## 🔄 Flujo Completo de Edición

1. Usuario hace click en **"Ver perfil"** (navbar o dashboard)
2. Vista de Perfil muestra toda la información
3. Click en **"Editar Perfil"**
4. Se abre `/edit-profile`
5. El componente `EditProfile.vue` detecta el tipo de usuario:
   - Si es Constructor → Muestra formulario de constructor
   - Si es Proveedor → Muestra formulario de proveedor
6. Usuario modifica campos
7. Submit → `PATCH` a la API
8. Éxito → Mensaje "✅ Perfil actualizado"
9. Se recarga el usuario del store
10. Cambios reflejados inmediatamente

---

## 📡 Endpoints API Utilizados

### Constructor
```bash
# Crear perfil
POST /api/constructor-profiles/
{
  "company_name": "...",
  "phone": "...",
  "city": "...",
  "region": "...",
  "address": "..."
}

# Editar perfil
PATCH /api/constructor-profiles/{user_id}/
```

### Proveedor
```bash
# Crear perfil (con FormData para logo)
POST /api/providers/
Content-Type: multipart/form-data
{
  "company_name": "...",
  "description": "...",
  "logo": [FILE],
  "phone": "...",
  "website": "...",
  "city": "...",
  "region": "...",
  "available_within_48h": true/false
}

# Editar perfil
PATCH /api/providers/{user_id}/
```

---

## 🎨 Estilos y UX

### Feedback Visual
- ✅ Mensajes de éxito en verde
- ❌ Mensajes de error en rojo
- ⚠️ Alertas en amarillo
- 🔄 Estados de carga (botones disabled)

### Validaciones
- Cliente: Campos requeridos antes de submit
- Servidor: Validación de Django/DRF

### Responsive
- Mobile-first design
- Grid adaptativo (1 col en móvil, 2-3 en desktop)
- Formularios optimizados para touch

---

## ✨ Mejoras Futuras Sugeridas

1. **Foto de perfil para Constructores**
   - Similar al logo de proveedores

2. **Geolocalización**
   - Autocompletar ciudad/región
   - Mapa de ubicación

3. **Verificación de Proveedor**
   - Subir documentos (RUT, certificados)
   - Proceso de aprobación por admin

4. **Rating y Reviews**
   - Mostrar valoraciones en perfil
   - Comentarios de constructores

5. **Portfolio de Trabajos**
   - Galería de proyectos realizados
   - Fotos de maquinaria en acción

---

## 🧪 Cómo Probar

### Test Constructor
```bash
1. Registrarse como Constructor
2. Ir a Dashboard → Ver alerta
3. Click "Crear Perfil Ahora"
4. Rellenar formulario
5. Submit
6. Verificar en Dashboard (alerta desaparece)
7. Ir a "Ver perfil" (navbar)
8. Click "Editar Perfil"
9. Cambiar datos
10. Submit
11. Verificar cambios
```

### Test Proveedor
```bash
1. Registrarse como Proveedor
2. Ir a Dashboard → Ver alerta
3. Click "Crear Perfil Ahora"
4. Rellenar formulario + subir logo
5. Activar "Disponible en < 48h"
6. Submit
7. Verificar en Dashboard:
   - Alerta desaparece
   - Toggle 48h visible
   - Datos de perfil en sidebar
8. Ir a "Ver perfil"
9. Ver logo, descripción, estadísticas
10. Click "Editar Perfil"
11. Cambiar datos + nuevo logo
12. Submit
13. Verificar cambios (nuevo logo visible)
```

---

## 📚 Navegación Rápida

```
/profile              → Ver mi perfil
/edit-profile         → Editar mi perfil
/constructor/create-profile  → Crear perfil constructor
/provider/create-profile     → Crear perfil proveedor
```

---

## 🎯 Resumen

✅ **Sistema de perfiles completo y funcional**
✅ **Interfaces visuales modernas con TailwindCSS**
✅ **Validación completa (cliente + servidor)**
✅ **Upload de imágenes con preview**
✅ **Alertas y notificaciones en dashboards**
✅ **Edición fluida con feedback inmediato**
✅ **Mobile-responsive**

---

**Fecha:** Noviembre 2025
**Proyecto:** ConnecMaq - Uber de Maquinaria Pesada
**Stack:** Vue 3 + Django + PostgreSQL

