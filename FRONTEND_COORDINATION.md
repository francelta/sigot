# 🔄 Coordinación Frontend - Migración del Wizard a Función Transaccional

**Fecha:** 2024-11-13  
**Agente:** Agente 5 (Ingeniero de Estado) → Agente 8 (Especialista en Dominio)  
**Prioridad:** 🔴 **ALTA** (Corrección de BUG #5 crítico)

---

## 📋 Resumen

El **Agente 5** ha creado una nueva función transaccional `submitOnboardingWizard()` que reemplaza las múltiples llamadas PATCH no transaccionales. El **Agente 8** debe refactorizar `OnboardingWizardView.vue` para usar esta nueva función.

---

## ✅ Cambios Realizados por Agente 5

### Nueva Función Creada

**Archivo:** `frontend/src/api/transportistas.ts`

**Función:** `submitOnboardingWizard(payload: WizardDataPayload)`

```typescript
export async function submitOnboardingWizard(
  payload: WizardDataPayload
): Promise<WizardSubmissionResponse>
```

### Tipo de Payload

```typescript
export interface WizardDataPayload {
  // Step 1: Datos de Negocio
  phone: string
  direccion_empresarial: string
  // Step 2: Zona de Actuación
  tipo_zona_actuacion: 'RADIO' | 'ZONAS'
  radio_km: number | null
  zonas_definidas: Record<string, unknown> | null
  // Step 3: Categorías
  categoria_ids: number[]
}
```

### Tipo de Response

```typescript
export interface WizardSubmissionResponse {
  message: string
  transportista: Transportista
  user: User
}
```

---

## 🔧 Tareas para Agente 8

### 1. Actualizar `OnboardingWizardView.vue`

**Archivo:** `frontend/src/views/OnboardingWizardView.vue`

**Cambios requeridos:**

1. **Importar la nueva función:**
   ```typescript
   import { submitOnboardingWizard } from '../api/transportistas'
   import type { WizardDataPayload } from '../api/transportistas'
   ```

2. **Reemplazar `updateMiPerfil` en `handleFinish()`:**
   
   **ANTES:**
   ```typescript
   const payload: UpdateMiPerfilPayload = {
     phone: wizardData.value.step1.phone || null,
     direccion_empresarial: wizardData.value.step1.direccion_empresarial || null,
     tipo_zona_actuacion: wizardData.value.step2.tipo_zona,
     categoria_ids: wizardData.value.step3.categoria_ids,
   }
   
   if (wizardData.value.step2.tipo_zona === 'RADIO') {
     payload.radio_km = wizardData.value.step2.radio_km
     payload.zonas_definidas = null
   } else {
     payload.radio_km = null
     payload.zonas_definidas = {
       tipo: wizardData.value.step2.zona_tipo,
     }
   }
   
   await updateMiPerfil(payload)
   ```

   **DESPUÉS:**
   ```typescript
   const payload: WizardDataPayload = {
     phone: wizardData.value.step1.phone,
     direccion_empresarial: wizardData.value.step1.direccion_empresarial,
     tipo_zona_actuacion: wizardData.value.step2.tipo_zona,
     radio_km: wizardData.value.step2.tipo_zona === 'RADIO' 
       ? wizardData.value.step2.radio_km 
       : null,
     zonas_definidas: wizardData.value.step2.tipo_zona === 'ZONAS'
       ? { tipo: wizardData.value.step2.zona_tipo }
       : null,
     categoria_ids: wizardData.value.step3.categoria_ids,
   }
   
   const response = await submitOnboardingWizard(payload)
   ```

3. **Actualizar el manejo de la respuesta:**
   
   **ANTES:**
   ```typescript
   // Refresh user profile in authStore
   const updatedUser = { ...authStore.user }
   if (updatedUser) {
     updatedUser.phone = wizardData.value.step1.phone || null
     authStore.user = updatedUser
     localStorage.setItem('auth_user', JSON.stringify(updatedUser))
   }
   ```

   **DESPUÉS:**
   ```typescript
   // Update authStore with response data (backend returns updated user and transportista)
   if (response.user) {
     authStore.user = response.user
     localStorage.setItem('auth_user', JSON.stringify(response.user))
   }
   ```

4. **Mantener el resto del flujo:**
   - Mantener `authStore.markOnboardingComplete()`
   - Mantener `router.push({ name: 'chats' })`
   - Mantener el manejo de errores (pero mejorar el mensaje de error)

---

## ⚠️ Notas Importantes

1. **Endpoint Backend:** El endpoint `/api/onboarding/complete/` debe estar implementado en el backend antes de usar esta función. Ver `BACKEND_COORDINATION.md`.

2. **Validación:** La nueva función espera que todos los campos requeridos estén presentes. Asegurar que la validación del wizard garantiza esto antes de llamar a `submitOnboardingWizard`.

3. **Manejo de Errores:** La función puede lanzar errores si:
   - El endpoint no existe (404)
   - La validación falla (400)
   - El usuario no está autenticado (401)
   - El usuario no es transportista (403)

   Mejorar el manejo de errores para mostrar mensajes específicos al usuario.

4. **Deprecación:** La función `updateMiPerfil` está marcada como `@deprecated` pero sigue disponible por compatibilidad. No debe usarse en nuevos flujos.

---

## 🧪 Testing

Después de la migración, verificar:

1. ✅ El wizard completa correctamente con todos los datos
2. ✅ Si falla la validación, se muestra un error claro
3. ✅ El perfil se actualiza completamente (no parcialmente)
4. ✅ El usuario se redirige a `/chats` después del éxito
5. ✅ El flag `perfilCompleto` se marca correctamente

---

## 📝 Checklist de Migración

- [x] Importar `submitOnboardingWizard` y `WizardDataPayload`
- [x] Reemplazar `updateMiPerfil` por `submitOnboardingWizard`
- [x] Construir el payload con el formato correcto
- [x] Actualizar el manejo de la respuesta para usar `response.user`
- [x] Mejorar mensajes de error
- [x] Probar el flujo completo
- [x] Verificar que no hay regresiones

---

**Estado:** ✅ Completado  
**Referencia:** `frontend/src/api/transportistas.ts` - Función `submitOnboardingWizard()`


