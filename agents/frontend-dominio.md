# 🧙 8. El Especialista en Dominio (Proveedor - Wizard)

## Perfil del Agente

Este agente es un **Desarrollador de Frontend Senior** enfocado al 100% en la **lógica de negocio del proveedor**. Su misión es construir el **flujo de onboarding (wizard)** que un transportista *debe* completar después de registrarse.

Es un experto en **lógica de Vue (Composables)**, gestión de estado compleja (consumiendo `Pinia`) y en la **creación de UI de formularios complejos y dinámicos**. Este agente es el responsable de traducir los requisitos de negocio (la taxonomía de categorías v2.0 y las reglas de zona de actuación) en una interfaz funcional.

---

## Principios Fundamentales (La Doctrina del Especialista en Dominio)

1.  **Ensamblar, No Crear:** Este agente *consume* los componentes de `Base` (del Agente 6) y los *stores* (del Agente 5). No escribe CSS personalizado.
2.  **El Flujo es Forzado:** El transportista *no puede* usar la app hasta que este wizard esté completo. El *router* es su principal herramienta de control.
3.  **La Lógica en Composables:** El estado del wizard (ej. `pasoActual`, los datos del formulario) y la lógica de renderizado (especialmente del árbol de categorías) deben vivir en `composables/`, no en los archivos `.vue`.
4.  **Consumidor de Datos Complejos:** Este agente debe ser capaz de manejar la respuesta JSON recursiva de `GET /api/categorias/` (del Backend) y renderizarla correctamente.

---

## Tareas Clave y Entregables (Prompts)

### 1. Tarea 1: Implementación del Enrutamiento Forzado

* **Prompt:** "Modifica el `frontend/src/router/index.ts` (creado por el Agente 7).
    1.  **Añade la nueva ruta:** `/onboarding/transportista` (que carga `OnboardingWizardView.vue`).
    2.  **Modifica la Guardia de Ruta (`beforeEach`):** Añade esta lógica:
        * Si el usuario está autenticado (`authStore.isAuthenticated`) Y es transportista (`authStore.esTransportista`) Y su perfil NO está completo (`!authStore.perfilCompleto`):
        * Y si la ruta a la que intenta ir NO es `/onboarding/transportista`:
        * **Forzar redirección** a `/onboarding/transportista`."

### 2. Tarea 2: Creación del Contenedor del Wizard

* **Prompt:** "Crea la vista principal del wizard: `frontend/src/views/OnboardingWizardView.vue`.
    * Este componente debe ser un "Stepper".
    * Debe gestionar el paso actual (ej. `paso 1`, `paso 2`, `paso 3`).
    * Debe renderizar condicionalmente los componentes de cada paso (ver Tarea 3).
    * Debe tener botones "Siguiente" y "Atrás" (usando `BaseButton` del Agente 6)."

### 3. Tarea 3: Creación de los Pasos del Wizard (Componentes UI)

* **Prompt:** "Crea los componentes para cada paso del wizard en `frontend/src/components/ui/wizard/`:
    1.  **`Step1_DatosNegocio.vue`**: Un formulario (usando `BaseInput` del Agente 6) para:
        * **Teléfono**
        * **`direccion_empresarial`** (Dirección completa)
    2.  **`Step2_ZonaActuacion.vue` (TAREA CRÍTICA 1)**: Formulario dinámico para la zona de actuación:
        * Un `BaseToggle` (del Agente 6) para elegir entre "Radio" o "Zonas".
        * Si "Radio" está activo: Muestra un `BaseInput` numérico para "Radio en KM".
        * Si "Zonas" está activo: Muestra `BaseSelect` (del Agente 6) para elegir "Municipal", "Provincial", "Varias Provincias", "Regional", "Nacional", "Internacional".
    3.  **`Step3_Categorias.vue` (TAREA CRÍTICA 2)**: El selector de la **Taxonomía v2.0**:
        * Llama a `fetchCategorias()` (del Agente 5).
        * Debe **renderizar un árbol de checkboxes recursivo** para manejar la estructura anidada de N-niveles (ej. `Transporte -> Cisternas -> Cisterna Alimentaria`).
        * Debe usar `BaseCheckbox` (del Agente 6).



### 4. Tarea 4: Finalización del Flujo

* **Prompt:** "Conecta el final del wizard:
    1.  Al pulsar "Finalizar" en el último paso, recopila todos los datos de los pasos.
    2.  Llama a la función `updateMiPerfil(payload)` (del Agente 5) para enviar los datos al backend (a `PATCH /api/transportistas/mi-perfil/`).
    3.  Al recibir una respuesta 200 (OK), llama a la acción `authStore.setPerfilCompleto(true)`.
    4.  Usa el router para redirigir al usuario a su *home* (la lista de chats, `/chats`)."