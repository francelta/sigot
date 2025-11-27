# 🔄 Coordinación Backend - Endpoint Transaccional de Onboarding

**Fecha:** 2024-11-13  
**Agente:** Agente 5 (Ingeniero de Estado)  
**Prioridad:** 🔴 **ALTA** (Corrección de BUG #5 crítico)

---

## 📋 Resumen

El frontend requiere un **nuevo endpoint transaccional** para completar el onboarding del transportista. Este endpoint debe procesar todos los datos del wizard en una **única transacción de base de datos** para evitar estados inconsistentes.

---

## 🎯 Endpoint Requerido

### Especificación

**Método:** `POST`  
**Ruta:** `/api/onboarding/complete/`  
**Autenticación:** Requerida (JWT Bearer Token)  
**Content-Type:** `application/json`

### Request Body

```json
{
  "phone": "+34612345678",
  "direccion_empresarial": "Calle Principal 123, Madrid, 28001",
  "tipo_zona_actuacion": "RADIO",
  "radio_km": 50,
  "zonas_definidas": null,
  "categoria_ids": [1, 2, 3]
}
```

**O para tipo ZONAS:**

```json
{
  "phone": "+34612345678",
  "direccion_empresarial": "Calle Principal 123, Madrid, 28001",
  "tipo_zona_actuacion": "ZONAS",
  "radio_km": null,
  "zonas_definidas": {
    "tipo": "NACIONAL"
  },
  "categoria_ids": [1, 2, 3]
}
```

### Campos Requeridos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `phone` | `string` | Teléfono del usuario (se actualiza en `User`) |
| `direccion_empresarial` | `string` | Dirección base de la empresa |
| `tipo_zona_actuacion` | `'RADIO' \| 'ZONAS'` | Tipo de zona de actuación |
| `radio_km` | `integer \| null` | Radio en km (solo si `tipo_zona_actuacion == 'RADIO'`) |
| `zonas_definidas` | `object \| null` | Zonas definidas (solo si `tipo_zona_actuacion == 'ZONAS'`) |
| `categoria_ids` | `array[integer]` | IDs de las categorías seleccionadas |

### Response (200 OK)

```json
{
  "message": "Onboarding completado exitosamente",
  "transportista": {
    "id": 1,
    "user": {
      "id": 1,
      "username": "transportista1",
      "email": "trans@example.com",
      "phone": "+34612345678",
      "is_transportista": true
    },
    "disponible": false,
    "direccion_empresarial": "Calle Principal 123, Madrid, 28001",
    "tipo_zona_actuacion": "RADIO",
    "radio_km": 50,
    "zonas_definidas": null,
    "categorias": [
      {
        "id": 1,
        "nombre": "Transporte de Mercancías",
        "descripcion": "..."
      }
    ]
  },
  "user": {
    "id": 1,
    "username": "transportista1",
    "email": "trans@example.com",
    "phone": "+34612345678",
    "is_transportista": true
  }
}
```

### Errores

**400 Bad Request:**
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Los datos proporcionados no son válidos",
  "details": {
    "phone": ["Este campo es requerido"],
    "radio_km": ["Debe ser mayor a 0 si tipo_zona_actuacion es RADIO"]
  }
}
```

**401 Unauthorized:**
```json
{
  "error": "UNAUTHORIZED",
  "message": "Token de autenticación inválido o expirado"
}
```

**403 Forbidden:**
```json
{
  "error": "FORBIDDEN",
  "message": "Solo los transportistas pueden completar el onboarding"
}
```

---

## 🔒 Requisitos de Implementación

### 1. Transaccionalidad

**CRÍTICO:** Todas las operaciones deben ejecutarse dentro de una **transacción de base de datos**:

```python
from django.db import transaction

@transaction.atomic
def complete_onboarding(request):
    # 1. Actualizar User.phone
    # 2. Actualizar/Crear Transportista con todos los campos
    # 3. Asignar categorías (ManyToMany)
    # Si cualquier paso falla, ROLLBACK completo
```

### 2. Validaciones

- Verificar que el usuario autenticado es transportista (`user.is_transportista == True`)
- Si `tipo_zona_actuacion == 'RADIO'`:
  - `radio_km` debe ser > 0
  - `zonas_definidas` debe ser `null`
- Si `tipo_zona_actuacion == 'ZONAS'`:
  - `radio_km` debe ser `null`
  - `zonas_definidas` debe tener al menos el campo `tipo`
- `categoria_ids` debe contener al menos 1 categoría válida
- Validar que todas las categorías existen en la BD

### 3. Geocodificación (Opcional para MVP)

Si el backend tiene geocodificación automática, puede procesar `direccion_empresarial` y actualizar `base_geocodificada`. Si no, dejarlo como `null` por ahora.

### 4. Respuesta

La respuesta debe incluir:
- El objeto `Transportista` completo (con relaciones)
- El objeto `User` actualizado
- Mensaje de confirmación

---

## 📝 Notas de Implementación

1. **Endpoint nuevo:** Este es un endpoint completamente nuevo, no modifica los existentes (`/transportistas/mi-perfil/`, `/auth/user/`).

2. **Compatibilidad:** El endpoint antiguo (`updateMiPerfil`) seguirá funcionando pero está marcado como `@deprecated` en el frontend.

3. **Testing:** Asegurar que:
   - Si falla la actualización de `User.phone`, no se actualiza `Transportista`
   - Si falla la asignación de categorías, se hace rollback de todo
   - Si una categoría no existe, se rechaza toda la operación

---

## 🔗 Referencias

- **Frontend:** `frontend/src/api/transportistas.ts` - Función `submitOnboardingWizard()`
- **Bug Report:** `QA_REPORT.md` - BUG #5
- **OpenAPI:** Actualizar `openapi.yml` con este nuevo endpoint

---

**Estado:** ✅ Completado  
**Asignado a:** Agente 3 (Backend Specialist)


