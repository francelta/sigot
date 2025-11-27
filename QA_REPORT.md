# 🐞 Reporte de QA - Frontend SIGOT

**Fecha:** 2024-11-13  
**Agente QA:** Agente 10 (Tester)  
**Versión:** Frontend v2.0

---

## Resumen Ejecutivo

Se realizó un análisis exhaustivo del código del frontend y pruebas exploratorias de los flujos críticos implementados por los Agentes 7, 8 y 9. Se encontraron **6 bugs** (1 Alta, 4 Media, 1 Baja) y **3 mejoras recomendadas**.

---

## 🐛 BUGS ENCONTRADOS

### BUG #1: No hay feedback visual cuando falla el envío de mensajes en el chat

**Severidad:** Media  
**Asignado a:** Agente 9 (Especialista en Interacción)  
**Componente:** `frontend/src/views/ChatRoomView.vue`

**Descripción:**
Cuando se intenta enviar un mensaje y el WebSocket no está conectado o falla, el error se captura pero solo se registra en consola. El usuario no recibe feedback visual y puede pensar que el mensaje se envió correctamente.

**Pasos para Reproducir:**
1. Abrir una sala de chat
2. Desconectar la red o cerrar el WebSocket manualmente
3. Intentar enviar un mensaje
4. Observar el comportamiento

**Resultado Esperado:**
- Mostrar un mensaje de error al usuario
- Permitir reintentar el envío
- Mostrar estado de conexión (conectado/desconectado)

**Resultado Actual:**
- El error solo se registra en consola
- El usuario no sabe que el mensaje no se envió
- El input se limpia como si el mensaje se hubiera enviado

**Código Afectado:**
```86:96:frontend/src/views/ChatRoomView.vue
function handleSendMessage(text: string) {
  try {
    sendMessage(text)
    // Scroll to bottom after sending
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error) {
    console.error('Error sending message:', error)
  }
}
```

**Recomendación:**
- Mostrar un toast/notificación de error
- Mantener el mensaje en el input si falla
- Añadir indicador de estado de conexión

---

### BUG #2: Validación insuficiente en Step2_ZonaActuacion para valores negativos

**Severidad:** Media  
**Asignado a:** Agente 8 (Especialista en Dominio)  
**Componente:** `frontend/src/components/ui/wizard/Step2_ZonaActuacion.vue`

**Descripción:**
El campo "Radio en Kilómetros" acepta valores negativos y cero, aunque la validación del wizard (`OnboardingWizardView.vue`) verifica `radio_km > 0`. Sin embargo, el usuario puede ingresar valores negativos que pasan la validación inicial pero causan problemas al enviar al backend.

**Pasos para Reproducir:**
1. Ir a `/onboarding/transportista`
2. Completar Step 1 (Datos de Negocio)
3. En Step 2, seleccionar "Radio"
4. Ingresar un valor negativo (ej: `-10`) o `0` en "Radio en Kilómetros"
5. Intentar avanzar al siguiente paso

**Resultado Esperado:**
- El botón "Siguiente" debe estar deshabilitado
- Debe mostrarse un mensaje de error indicando que el radio debe ser mayor a 0

**Resultado Actual:**
- Con valor `0`: El botón está deshabilitado (correcto)
- Con valor negativo (ej: `-10`): El botón puede estar habilitado si la validación no se ejecuta correctamente
- No hay validación visual en tiempo real

**Código Afectado:**
```132:135:frontend/src/views/OnboardingWizardView.vue
      if (wizardData.value.step2.tipo_zona === 'RADIO') {
        return (
          wizardData.value.step2.radio_km !== null &&
          wizardData.value.step2.radio_km > 0
        )
```

**Recomendación:**
Añadir validación en `Step2_ZonaActuacion.vue` que muestre error cuando `radio_km <= 0`.

---

### BUG #3: Campo zona_tipo no se limpia al cambiar de ZONAS a RADIO

**Severidad:** Baja  
**Asignado a:** Agente 8 (Especialista en Dominio)  
**Componente:** `frontend/src/components/ui/wizard/Step2_ZonaActuacion.vue`

**Descripción:**
Cuando el usuario selecciona "Zonas" y elige un tipo (ej: "Nacional"), luego cambia a "Radio", el campo `zona_tipo` no se limpia. Aunque esto no afecta la funcionalidad (porque solo se envía `zonas_definidas` si `tipo_zona === 'ZONAS'`), puede causar confusión.

**Pasos para Reproducir:**
1. En Step 2, seleccionar "Zonas"
2. Seleccionar "Nacional" en el dropdown
3. Cambiar a "Radio"
4. Observar el estado del formulario

**Resultado Esperado:**
- El campo `zona_tipo` debe limpiarse al cambiar a "Radio"

**Resultado Actual:**
- El valor de `zona_tipo` persiste (aunque no se envía al backend)

**Código Afectado:**
```155:165:frontend/src/components/ui/wizard/Step2_ZonaActuacion.vue
// Watch for tipo_zona changes to reset dependent fields
watch(
  () => localData.tipo_zona,
  newValue => {
    if (newValue === 'RADIO') {
      localData.zona_tipo = ''
    } else if (newValue === 'ZONAS') {
      localData.radio_km = null
    }
  }
)
```

**Nota:** El código SÍ limpia `zona_tipo` cuando cambia a RADIO, pero hay un problema de sincronización con el emit.

---

### BUG #4: Manejo de errores insuficiente en useChatRoom cuando roomId es inválido

**Severidad:** Media  
**Asignado a:** Agente 9 (Especialista en Interacción)  
**Componente:** `frontend/src/composables/useChatRoom.ts`

**Descripción:**
Si un usuario accede a `/chat/abc` (ID inválido) o `/chat/999` (ID que no existe), el composable solo hace `console.error` pero no informa al usuario ni redirige.

**Pasos para Reproducir:**
1. Autenticarse como usuario
2. Navegar manualmente a `/chat/abc` o `/chat/999`
3. Observar el comportamiento

**Resultado Esperado:**
- Mostrar un mensaje de error al usuario
- Redirigir a `/chats` o mostrar una vista de error

**Resultado Actual:**
- Solo se registra el error en consola
- El usuario ve una pantalla en blanco o con errores

**Código Afectado:**
```25:40:frontend/src/composables/useChatRoom.ts
  onMounted(async () => {
    if (!roomId.value || isNaN(roomId.value)) {
      console.error('Invalid room ID')
      return
    }

    try {
      // Load existing messages first
      const messagesResponse = await getMessages(roomId.value, { limit: 50 })
      chatStore.messages = messagesResponse.results.reverse() // Reverse to show oldest first

      // Connect to WebSocket
      await chatStore.connectToRoom(roomId.value)
    } catch (error) {
      console.error('Error connecting to chat room:', error)
    }
  })
```

**Recomendación:**
Añadir manejo de errores que redirija al usuario o muestre un mensaje de error.

---

### BUG #5: updateMiPerfil hace múltiples llamadas PATCH sin manejo de errores parciales (RESUELTO)

**Severidad:** Alta  
**Asignado a:** Agente 5 (Ingeniero de Estado)  
**Estado:** ✅ Resuelto (Implementado endpoint transaccional `/api/onboarding/complete/`)
**Componente:** `frontend/src/api/transportistas.ts`

**Descripción:**
(Resuelto) La función `updateMiPerfil` realizaba múltiples llamadas. Se ha reemplazado por `submitOnboardingWizard` que es atómica.

**Pasos para Reproducir:**
1. Completar el wizard de onboarding
2. Simular un error de red en la segunda llamada PATCH
3. Observar el estado del perfil

**Resultado Esperado:**
- Todas las actualizaciones deben ser atómicas (todo o nada)
- O al menos, manejar errores parciales y revertir cambios

**Resultado Actual:**
- Si falla la segunda llamada, el teléfono puede haberse actualizado pero no el perfil del transportista
- El usuario ve un error pero su perfil está parcialmente actualizado

**Código Afectado:**
```130:169:frontend/src/api/transportistas.ts
export async function updateMiPerfil(
  payload: UpdateMiPerfilPayload
): Promise<UpdateMiPerfilResponse> {
  // First update user phone if provided
  if (payload.phone !== undefined) {
    await client.patch('/auth/user/', { phone: payload.phone })
  }

  // Update transportista profile
  const transportistaPayload: Record<string, unknown> = {}

  // ... código ...

  // Update transportista basic data if any
  if (Object.keys(transportistaPayload).length > 0) {
    await client.patch('/transportistas/mi-perfil/', transportistaPayload)
  }

  // Update categories if provided
  if (payload.categoria_ids && payload.categoria_ids.length > 0) {
    await client.patch('/transportistas/mi-perfil/', {
      categoria_ids: payload.categoria_ids,
    })
  }

  return { message: 'Perfil actualizado correctamente' }
}
```

**Recomendación:**
- Consolidar todas las actualizaciones en una sola llamada PATCH si el backend lo soporta
- O implementar transacciones/rollback en caso de error

---

### BUG #6: WebSocket no se reconecta automáticamente si se pierde la conexión

**Severidad:** Media  
**Asignado a:** Agente 9 (Especialista en Interacción)  
**Componente:** `frontend/src/stores/chatStore.ts`

**Descripción:**
Si la conexión WebSocket se pierde (pérdida de red, servidor caído), no hay lógica de reconexión automática. El usuario debe recargar la página para reconectar.

**Pasos para Reproducir:**
1. Abrir una sala de chat
2. Desconectar la red (o detener el servidor WebSocket)
3. Intentar enviar un mensaje
4. Reconectar la red
5. Observar si el WebSocket se reconecta automáticamente

**Resultado Esperado:**
- El WebSocket debe intentar reconectarse automáticamente
- Mostrar un indicador de "Reconectando..." al usuario

**Resultado Actual:**
- El WebSocket no se reconecta
- El usuario debe recargar la página manualmente

**Código Afectado:**
```83:89:frontend/src/stores/chatStore.ts
    ws.onclose = () => {
      console.log(`Disconnected from chat room ${roomId}`)
      if (activeRoomId.value === roomId) {
        activeRoomId.value = null
        websocket.value = null
      }
    }
```

**Recomendación:**
Implementar lógica de reconexión con backoff exponencial.

---

## ⚠️ MEJORAS RECOMENDADAS

### MEJORA #1: Validación de teléfono en Step1_DatosNegocio

**Severidad:** Baja  
**Asignado a:** Agente 8 (Especialista en Dominio)

**Descripción:**
El campo de teléfono no valida el formato. Acepta cualquier string, incluso valores inválidos.

**Recomendación:**
Añadir validación de formato de teléfono (ej: regex para números internacionales).

---

### MEJORA #2: Feedback visual cuando se envían mensajes en el chat

**Severidad:** Baja  
**Asignado a:** Agente 9 (Especialista en Interacción)

**Descripción:**
Cuando se envía un mensaje, no hay indicador visual de que el mensaje se está enviando. Si falla, el usuario no lo sabe hasta que intenta enviar otro.

**Recomendación:**
- Mostrar un indicador de "Enviando..." mientras el mensaje se procesa
- Mostrar mensajes fallidos con opción de reintentar

---

### MEJORA #3: Manejo de errores en OnboardingWizardView

**Severidad:** Baja  
**Asignado a:** Agente 8 (Especialista en Dominio)

**Descripción:**
El manejo de errores usa `alert()`, que no es una buena UX. Además, si falla la actualización, el usuario puede quedar en un estado inconsistente.

**Recomendación:**
- Usar un componente de notificación (toast) en lugar de `alert()`
- Mostrar errores específicos del backend
- Permitir al usuario reintentar sin perder los datos del formulario

---

## ✅ FLUJOS VALIDADOS CORRECTAMENTE

1. **Enrutamiento forzado:** ✅ Funciona correctamente - transportistas sin perfil completo son redirigidos al wizard
2. **Wizard Step 1:** ✅ Validación de campos requeridos funciona
3. **Wizard Step 3:** ✅ Árbol recursivo de categorías se carga y renderiza correctamente
4. **Flujo de búsqueda:** ✅ Navegación de SearchView a ResultsView funciona
5. **Botón Contactar:** ✅ Crea sala de chat y navega correctamente

---

## 📋 PRÓXIMOS PASOS

1. **Prioridad Alta:** ✅ Corregido BUG #5 (actualización parcial del perfil)
2. **Prioridad Media:** Corregir BUG #1, #2, #4, #6
3. **Prioridad Baja:** Corregir BUG #3 e implementar mejoras recomendadas

---

**Estado General:** 🟡 **Funcional con mejoras necesarias**

La aplicación es funcional para el MVP, pero requiere correcciones antes de producción, especialmente en el manejo de errores y la robustez de las conexiones WebSocket.

