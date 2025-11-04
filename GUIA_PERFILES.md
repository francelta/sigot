# 🚀 Guía Rápida: Sistema de Perfiles

## ✅ ¿Qué se ha implementado?

Sistema completo de **creación y edición de perfiles** para Constructores y Proveedores con:
- ✨ Interfaces visuales modernas
- 📸 Upload de imágenes (proveedores)
- ⚡ Toggle "Disponible en < 48h"
- ✅ Validación completa
- 📱 Mobile responsive

---

## 🎯 Cómo Usar

### Para Constructores

#### 1️⃣ Crear Perfil
```
1. Iniciar sesión como Constructor
2. Ir al Dashboard
3. Ver alerta amarilla: "Completa tu perfil"
4. Click en "Crear Perfil Ahora"
5. Llenar formulario:
   - Nombre de empresa ✅ (obligatorio)
   - Teléfono
   - Dirección
   - Ciudad ✅ (obligatorio)
   - Región ✅ (obligatorio)
6. Click "Crear Perfil"
7. ✅ ¡Perfil creado!
```

#### 2️⃣ Editar Perfil
```
1. Click en "Ver perfil" (navbar o dashboard)
2. Click en "Editar Perfil"
3. Modificar los campos que necesites
4. Click "Guardar Cambios"
5. ✅ Perfil actualizado
```

---

### Para Proveedores

#### 1️⃣ Crear Perfil
```
1. Iniciar sesión como Proveedor
2. Ir al Dashboard
3. Ver alerta amarilla: "Completa tu perfil de proveedor"
4. Click en "Crear Perfil Ahora"
5. Llenar formulario:
   - Nombre de empresa ✅ (obligatorio)
   - Descripción de la empresa
   - Logo 📸 (opcional, máx 2MB)
   - Teléfono ✅ (obligatorio)
   - Sitio web
   - Dirección
   - Ciudad ✅ (obligatorio)
   - Región ✅ (obligatorio)
6. Activar/desactivar ⚡ "Disponible en < 48h"
7. Click "Crear Perfil"
8. ✅ ¡Perfil creado!
```

#### 2️⃣ Editar Perfil
```
1. Click en "Ver perfil" (navbar)
2. Click en "Editar Perfil"
3. Modificar los campos que necesites
4. Para cambiar logo: Seleccionar nueva imagen
   (Si no seleccionas, se mantiene la anterior)
5. Cambiar toggle "Disponible en < 48h" si es necesario
6. Click "Guardar Cambios"
7. ✅ Perfil actualizado
```

---

## 🔍 Verificar Perfil

### Ver tu perfil completo
```
Navbar → "Ver perfil"
```

Verás:
- 📧 Información de usuario (email, username)
- 🏢 Información de empresa
- 📊 Estadísticas (proveedores)
- 🔔 Estado de suscripción (proveedores)

---

## ⚡ Toggle "Disponible en < 48h"

### ¿Qué hace?

Este toggle es **clave** en ConnecMaq:

✅ **Activado:**
- Apareces en búsquedas prioritarias
- Constructores te encuentran cuando buscan servicio inmediato
- Indicador verde en tu perfil

❌ **Desactivado:**
- No apareces en búsquedas de "servicio rápido"
- Aún puedes recibir consultas normales

### Cómo cambiarlo

**Opción 1: En el Dashboard**
```
Dashboard → Toggle en la esquina superior derecha
✓ Disponible 48h / No disponible
```

**Opción 2: En Editar Perfil**
```
Editar Perfil → Checkbox "Disponible en menos de 48 horas"
```

---

## 📸 Subir Logo (Proveedores)

### Requisitos
- Formato: JPG, PNG, GIF
- Tamaño máximo: **2 MB**

### Proceso
```
1. Click en "Examinar" / "Choose file"
2. Seleccionar imagen
3. Ver preview inmediato 👁️
4. Si no te gusta, selecciona otra
5. Submit formulario
```

### Cambiar Logo
```
1. Ir a Editar Perfil
2. Ver logo actual
3. Seleccionar nueva imagen (opcional)
4. Si no seleccionas nada, se mantiene la anterior
5. Guardar
```

---

## 🎨 Alertas y Mensajes

### Alerta: "Completa tu perfil"
- **Cuándo aparece:** Si no tienes perfil creado
- **Dónde:** Dashboard (arriba)
- **Color:** Amarillo ⚠️
- **Acción:** Click "Crear Perfil Ahora"

### Mensaje: "Perfil creado exitosamente"
- **Cuándo:** Después de crear perfil
- **Color:** Verde ✅
- **Duración:** 1 segundo (luego redirección)

### Mensaje: "Perfil actualizado exitosamente"
- **Cuándo:** Después de editar perfil
- **Color:** Verde ✅
- **Duración:** 3 segundos

### Mensaje de Error
- **Cuándo:** Si hay problemas (campos vacíos, imagen muy grande, etc.)
- **Color:** Rojo ❌
- **Acción:** Corregir y reintentar

---

## 📱 Navegación

### Rutas Principales
```
/profile                        → Ver mi perfil
/edit-profile                   → Editar mi perfil
/constructor/create-profile     → Crear perfil constructor
/provider/create-profile        → Crear perfil proveedor
```

### Desde el Navbar
```
Click en "Ver perfil" → Vista completa del perfil
```

### Desde el Dashboard
```
Constructor:
- Tarjeta "Mi Perfil" → Click "Ver perfil →"

Proveedor:
- Tarjeta "Mi Perfil" → Click "Editar perfil →"
- O sidebar derecho con datos de perfil
```

---

## ❓ Preguntas Frecuentes

### ¿Es obligatorio crear el perfil?

**No es obligatorio**, pero es **altamente recomendado**:
- Constructores: Para poder solicitar servicios
- Proveedores: **Obligatorio** para listar maquinaria

### ¿Puedo cambiar mi perfil después?

**Sí**, todas las veces que quieras:
1. Ir a "Ver perfil"
2. Click "Editar Perfil"
3. Modificar
4. Guardar

### ¿Puedo tener perfil de Constructor Y Proveedor?

**Sí**, si marcaste ambas opciones al registrarte, puedes crear ambos perfiles.

### ¿Qué pasa si subo una imagen muy grande?

El sistema te avisará:
```
❌ "La imagen no debe superar 2MB"
```
Debes comprimir o elegir otra imagen.

### ¿Los demás usuarios ven mi perfil?

**Constructores:** Tu perfil es privado (solo tú lo ves)

**Proveedores:** Tu perfil es **público**:
- Aparece en búsquedas
- Los constructores pueden ver tu empresa, descripción, logo
- Tus datos de contacto solo se muestran cuando inician chat

---

## 🔧 Solución de Problemas

### "Error al crear el perfil"
✅ **Solución:**
- Verifica que hayas llenado todos los campos obligatorios (*)
- Si es proveedor, verifica que la imagen sea < 2MB
- Intenta nuevamente

### "No veo el botón 'Crear Perfil'"
✅ **Solución:**
- Verifica que hayas iniciado sesión
- Verifica que no tengas ya un perfil creado
- Recarga la página (F5)

### "Cambié el logo pero no se ve"
✅ **Solución:**
- Refresca la página (F5)
- Limpia caché del navegador
- Verifica que el archivo se haya subido (< 2MB)

### "El toggle 48h no aparece"
✅ **Solución:**
- Solo visible para proveedores
- Solo visible si ya tienes perfil creado
- Intenta desde el Dashboard

---

## 📞 Campos del Formulario

### Constructor
| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| Nombre de empresa | ✅ | Tu empresa constructora |
| Teléfono | ❌ | Contacto |
| Dirección | ❌ | Ubicación física |
| Ciudad | ✅ | Ciudad |
| Región | ✅ | Región |

### Proveedor
| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| Nombre de empresa | ✅ | Tu empresa proveedora |
| Descripción | ❌ | Describe tus servicios |
| Logo | ❌ | Imagen (máx 2MB) |
| Teléfono | ✅ | Contacto |
| Sitio web | ❌ | URL de tu sitio |
| Dirección | ❌ | Ubicación física |
| Ciudad | ✅ | Ciudad |
| Región | ✅ | Región |
| Disponible < 48h | ❌ | Toggle (default: Sí) |

---

## ✨ Resumen

1. **Registrarse** → Login
2. **Ir al Dashboard** → Ver alerta si no tienes perfil
3. **Crear Perfil** → Llenar formulario
4. **Editar cuando quieras** → Ver perfil → Editar
5. **Toggle 48h** (proveedores) → Activar/desactivar

---

¡Listo! 🎉 Tu perfil está configurado y puedes empezar a usar ConnecMaq.

