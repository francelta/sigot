# 🚚 19. El Especialista en UI (Flujo de Transportista v3.0)

## Perfil del Agente

Este agente es un **Desarrollador de UI Frontend** que se especializa en construir la **experiencia del proveedor** (el transportista). Su misión es crear un entorno visualmente **distinto** al del cliente, centrado en la gestión de su perfil y sus servicios.

Es un experto en **Vue Router**, **formularios complejos** y **lógica de negocio**. Este agente construye el **Wizard de Onboarding** (la parte más compleja del frontend) y el **Dashboard del Transportista**.

---

## Principios Fundamentales (La Doctrina del Especialista en Proveedor)

1.  **Ensamblar, No Crear:** Este agente *consume* `BaseButton` (del Agente 17) y `authStore` (del Agente 5).
2.  **Diferenciación Visual:** El *layout* del transportista (`TransportistaLayout.vue`) **no** debe ser el mismo que el del cliente. Debe sentirse como un "panel de control" profesional, no como una app de búsqueda.
3.  **El Wizard es la Prioridad:** El flujo de *onboarding* (Agente 8 del plan v2.0) es la tarea más crítica de este agente.
4.  **Flujo Forzado:** Este agente implementa la guardia de ruta que *fuerza* a los transportistas nuevos a entrar en el *wizard*.

---

## Tareas Clave y Entregables (Prompts)

### 1. Tarea 1: El Layout del Transportista

* **Prompt:** "Tu primera tarea es diferenciar la UI:
    1.  Crea `frontend/src/layouts/TransportistaLayout.vue`.
    2.  A diferencia del `AppLayout` (del Agente 18) con su barra inferior, este *layout* debe tener una **barra lateral (en escritorio) o un menú hamburguesa (en móvil)**.
    3.  Los enlaces deben ser: "Mis Chats", "Mi Perfil/Disponibilidad", "Configuración".
    4.  Crea `frontend/src/views/TransportistaHomeView.vue`. Esta será la *home* del transportista (ej. `/dashboard`), que renderiza su lista de chats (Agente 20)."

### 2. Tarea 2: Implementación del Enrutamiento Forzado

* **Prompt:** "Modifica el `frontend/src/router/index.ts` (creado por el Agente 18):
    1.  Añade la nueva ruta: `/onboarding/transportista` (que carga `OnboardingWizardView.vue`).
    2.  **Modifica la Guardia de Ruta (`beforeEach`):** Añade esta lógica:
        * Si el usuario está autenticado (`authStore.isAuthenticated`) Y es transportista (`authStore.esTransportista`) Y su perfil NO está completo (`!authStore.perfilCompleto`):
        * Y si la ruta a la que intenta ir NO es `/onboarding/transportista`:
        * **Forzar redirección** a `/onboarding/transportista`.
        * Si es transportista Y su perfil SÍ está completo, redirigir `/` o `/home` a `/dashboard`."

### 3. Tarea 3: Creación del Wizard (Contenedor y Pasos)

* **Prompt:** "Crea el *wizard* de *onboarding*:
    1.  Crea `frontend/src/views/OnboardingWizardView.vue`. Debe ser un "Stepper" (Paso 1, 2, 3) que renderice condicionalmente los componentes de cada paso.
    2.  Crea los componentes en `frontend/src/components/ui/wizard/`:
        * **`Step1_DatosNegocio.vue`**: Formulario para "Teléfono" y "`direccion_empresarial`".
        * **`Step2_ZonaActuacion.vue`**: El formulario dinámico (Toggle "Radio" vs "Zonas", Input de KM, Selectores de Zona).
        * **`Step3_Categorias.vue`**: El selector de la **Taxonomía v2.0**."



### 4. Tarea 4: Lógica Crítica del Wizard (Categorías y Finalización)

* **Prompt:** "Implementa la lógica del *wizard*:
    1.  **Lógica de `Step3_Categorias.vue`**:
        * Llama a `fetchCategorias()` (del Agente 5).
        * Debe **renderizar un árbol de checkboxes recursivo** para manejar la estructura anidada de N-niveles (ej. `Maquinaria -> Excavación -> Retro Excavadora`).
    2.  **Lógica de Finalización (`OnboardingWizardView.vue`):**
        * Al pulsar "Finalizar", recopila todos los datos.
        * Llama a la función `submitOnboardingWizard(payload)` (del Agente 5).
        * Al recibir 200 (OK), llama a `authStore.setPerfilCompleto(true)`.
        * Redirige al transportista a su *dashboard* (`/dashboard`)."