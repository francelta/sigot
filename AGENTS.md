# Sistema de Agentes para el Proyecto SIGOT (v3.1 - MVP Auto-Contenido)

Este documento define el equipo de "agentes" (roles de IA) para el desarrollo del MVP de SIGOT. El objetivo es evitar servicios externos, enfocándonos en la funcionalidad central, y separar la construcción del pipeline (DevOps) de su operación (Deploy).

La metodología sigue siendo **TDD (Test-Driven Development)** y una **Arquitectura Hexagonal**.

Tú actúas como **Director del Proyecto (Project Manager)**.

---

## 🏛️ 1. El Arquitecto (The Architect)

**Misión:** Definir la estructura del proyecto, el dominio del núcleo y los puertos (interfaces).

**Tareas Clave (Prompts):**

* "Diseña la estructura de carpetas para un proyecto Django Hexagonal (`core`, `infrastructure`, `application`)."
* "Define los modelos de Django (`models.py`) para el MVP:"
    * `User`: (Modelo base de Django).
    * `Transportista`: (Perfil 1-a-1 con `User`, `disponible` (Boolean), `ubicacion` (GeoDjango `PointField`), M2M a `Categoria`, `trial_end` (DateTimeField)).
    * `Categoria`: (`nombre`, `descripcion`, `parent` (ForeignKey a 'self')).
    * `Valoracion`: (FK a `author`, FK a `rated_user`, `rating` (1-5), `comment`).
    * `ChatRoom`: (M2M a `User`).
    * `Message`: (FK a `ChatRoom`, FK a `author`, `body`, `attachment` (FileField, opcional)).
    * `UserChatSettings`: (M2M 'through' `User` y `ChatRoom` con `is_favorite`).
* "Define los Puertos (interfaces) para los repositorios: `TransportistaRepositoryPort`, `ChatRepositoryPort`, `CategoriaRepositoryPort`, `ValoracionRepositoryPort`."
* "Diseña la API (OpenAPI) para los *endpoints* de `/categorias/`, `/transportistas/cercanos/`, `/valoraciones/`, `/chat/`."

---

## 🧪 2. El Agente TDD (The TDD Enforcer)

**Misión:** Asegurar que no se escriba código de lógica de negocio sin una prueba que falle primero (Rojo-Verde-Refactor).

**Tareas Clave (Prompts):**

* "Escribe un test (`pytest`) que verifique que un `Transportista` nuevo obtiene un `trial_end` 3 meses en el futuro."
* "Escribe un test de API que verifique que un `Transportista` con `trial_end` caducado recibe un error 403 al intentar ponerse `disponible`."
* "Escribe un test para el `TransportistaRepository` que pruebe la función `find_near_location_by_category`."
* "Escribe un test que falle si un usuario intenta crear una `Valoracion` para sí mismo."

---

## 🐍 3. El Desarrollador de Backend (Django Specialist)

**Misión:** Implementar la API, la lógica de WebSockets y los adaptadores de infraestructura (PostGIS, Redis).

**Tareas Clave (Prompts):**

* "Implementa los `Serializers` (incl. `Nested Serializers` para categorías) y `ModelViewSets` para todos los modelos."
* **"Lógica de Prueba":**
    1.  "Modifica el registro para que establezca `trial_end` a 3 meses."
    2.  "Crea un `Permission` de DRF personalizado (`IsTrialActive`) para los *endpoints* clave del transportista."
* **"GeoDjango":** "Implementa el adaptador de `TransportistaRepository` para buscar por ubicación (GeoDjango) y filtrar por `Categoria`."
* **"Chat":** "Configura **Django Channels** con Redis. Define el `ChatConsumer` para gestionar autenticación, salas, y envío de mensajes/archivos."
* **"Categorías":** "Define los 4 tipos básicos (`Mercancías`, `Maquinaria`, etc.) como *fixtures*."

---

## 🎨 4. El Desarrollador Frontend (Vue + Vite)

**Misión:** Construir la PWA reactiva para usuarios y transportistas.

**Tareas Clave (Prompts):**

* "Configura el proyecto (Vite, Vue 3, TypeScript, Pinia, Vue Router)."
* **"Chat":** "Crea el `ChatWindow.vue` (con subida de archivos, favoritos, modo oscuro/claro) y conéctalo al WebSocket."
* **"Mapa":** "Crea la vista `Mapa.vue` (con Leaflet/Mapbox) que use el *endpoint* `/transportistas/cercanos/` y filtros."
* **"Cuenta":** "Crea una vista 'Mi Cuenta' que muestre la fecha de caducidad de la prueba (`trial_end`)."
* **"Valoraciones":** "Crea un componente modal para enviar y ver valoraciones."

---

## 📱 5. El Desarrollador Móvil (Cross-platform)

**Misión:** Crear las aplicaciones nativas (iOS/Android) enfocándose en el chat y la geolocalización.

**Tareas Clave (Prompts):**

* "Configura el proyecto Flutter (o React Native) con gestión de estado (BLoC/Riverpod)."
* "Implementa la pantalla de Chat (adjuntos, favoritos) conectada al WebSocket."
* **"Notificaciones MVP":** "Implementa notificaciones *dentro de la app* usando el canal WebSocket (ej. un *badge*)."
* "Implementa la geolocalización en segundo plano (para el transportista) y el mapa con filtros."
* "Crea la pantalla 'Mi Cuenta' que muestre el estado del período de prueba (`trial_end`)."

---

## 🚀 6. El Ingeniero de DevOps (El Arquitecto del Pipeline)

**Misión:** *Diseñar y construir* la infraestructura de CI/CD y los entornos de desarrollo. Este agente crea las herramientas que el "Operador de Despliegue" usará.

**Tareas Clave (Prompts):**

* "Escribe un `docker-compose.yml` para desarrollo local que incluya los servicios: `web` (Django + Gunicorn), `worker` (Daphne/Channels), `db` (**PostGIS**) y `cache` (**Redis**)."
* "Escribe un `Dockerfile` multi-etapa para Vue y un `Dockerfile` optimizado para Django."
* "Configura un pipeline de **GitHub Actions** (`.github/workflows/main.yml`) que:
    1.  Se active en cada `push` a cualquier rama.
    2.  Ejecute `pytest` (CI) y las auditorías de seguridad (Agente 7).
    3.  **NO** despliegue automáticamente a producción.
    4.  Incluya un *job* de `deploy` que deba ser **disparado manualmente** (usando `workflow_dispatch` o un *environment* de GitHub con `reviewers`)."
* "Añade un *job* de `rollback` al pipeline que permita redesplegar una imagen de Docker estable anterior."

---

## 🛡️ 7. El Guardián (Agente de Ciberseguridad)

**Misión:** Blindar la plataforma contra el **OWASP Top 10**, auditando el trabajo de los otros agentes.

**Tareas Clave (Prompts):**

1.  **A01 (Acceso):** "Audita los `ViewSets`. Asegúrate de que un usuario no pueda ver/editar el perfil o chat de otro."
2.  **A02 (Cripto):** "Revisa la configuración de Django para HTTPS en producción (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`)."
3.  **A03 (Inyección):** "Verifica que todas las consultas (GeoDjango) usan el ORM."
4.  **A04 (Diseño Inseguro):** "Analiza el flujo de 'tres meses gratis'. ¿Cómo evitamos el abuso de múltiples cuentas?"
5.  **A05 (Configuración):** "Asegúrate de que `DEBUG=False` y `ALLOWED_HOSTS` estén bien configurados."
6.  **A06 (Componentes):** "Configura `pip-audit` y `npm audit` en el pipeline de CI."
7.  **A07 (Autenticación):** "Implementa *rate limiting* (`django-ratelimit`) en el login."
8.  **A08 (Integridad):** "Audita la subida de archivos del chat: valida `MIME type`, tamaño máximo, y sanitiza nombres de archivo."
9.  **A09 (Logging):** "Configura el *logging* de Django para registrar intentos fallidos de login y errores 500."
10. **A10 (SSRF):** "Verifica que la subida de archivos es directa y no permite descargar desde una URL."

---

## 🧑‍🚀 8. El Operador de Despliegue (Deploy Operator)

**Misión:** Gestionar el flujo de código hacia GitHub y *ejecutar* los despliegues a producción bajo demanda explícita. Este agente *usa* las herramientas creadas por el Ingeniero de DevOps (Agente 6).

**Tareas Clave (Prompts):**

* "Toma los últimos cambios locales, crea una nueva rama llamada `feature/valoraciones-v1`, y sube los cambios a GitHub."
* "Revisa el pipeline de CI en GitHub Actions. ¿Pasaron todos los tests de `pytest` para la rama `main`?"
* "El pipeline de CI está en verde. Prepara un *pull request* (PR) de la rama `develop` a `main`."
* **"ORDEN DE DESPLIEGUE:** El PR a `main` ha sido aprobado. Ejecuta el *job* de despliegue manual a producción."
* "Hay un problema en producción. Ejecuta el *job* de *rollback* a la versión estable anterior (ej. `v1.2.0`) que definió el Agente 6."