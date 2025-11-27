# 🏛️ Arquitectura Hexagonal de SIGOT

Este documento define la estructura de directorios del proyecto SIGOT y establece las **reglas fundamentales** que todos los desarrolladores deben seguir.

## Estructura de Directorios

```
sigot/
├── core/                    # 🎯 DOMINIO PURO - El Corazón del Negocio
│   ├── entities/           # Entidades POPO/dataclasses (sin Django)
│   ├── ports.py            # Interfaces (Puertos) - Contratos del núcleo
│   └── services/           # Lógica de negocio pura
│
├── application/            # 🔄 CASOS DE USO - Orquestación
│   └── use_cases/          # Servicios de aplicación que orquestan el flujo
│
├── infrastructure/         # 🔌 ADAPTADORES - Detalles de Implementación
│   ├── db/                 # Adaptador de Base de Datos
│   │   ├── models.py       # Modelos de Django (ORM)
│   │   └── repositories/   # Implementaciones de repositorios (ORM)
│   ├── api/                # Adaptador de API REST
│   │   ├── serializers.py  # Serializers de DRF
│   │   └── viewsets.py      # ViewSets de DRF
│   └── websockets/         # Adaptador de WebSockets
│       └── consumers.py    # Consumers de Django Channels
│
└── boot/                   # ⚙️ CONFIGURACIÓN - Bootstrap de Django
    ├── settings.py         # Configuración de Django
    ├── urls.py             # URLs principales
    ├── wsgi.py             # WSGI para producción
    └── asgi.py             # ASGI para Channels
```

---

## 🚨 Reglas Fundamentales (La Doctrina)

### 1. **Separación de Capas (Ley de Dependencias)**

```
application → core ← infrastructure
     ↓           ↑
     └───────────┘
```

**Regla:** Las dependencias SOLO pueden apuntar hacia adentro:
- `core/` **NO puede importar** nada de `application/` ni `infrastructure/`
- `application/` **puede importar** de `core/` pero **NO de `infrastructure/`**
- `infrastructure/` **puede importar** de `core/` y `application/`

### 2. **Core es Puro (Sin Framework)**

El directorio `core/` es **100% agnóstico de framework**:
- ❌ **PROHIBIDO:** `from django.db import models`
- ❌ **PROHIBIDO:** `from rest_framework import serializers`
- ✅ **PERMITIDO:** `from abc import ABC, abstractmethod`
- ✅ **PERMITIDO:** `from dataclasses import dataclass`
- ✅ **PERMITIDO:** Lógica de negocio pura en Python

**Ejemplo de entidad en `core/`:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transportista:
    id: int
    user_id: int
    disponible: bool
    trial_end: datetime
```

### 3. **Puertos (Interfaces) en Core**

Los **Puertos** (interfaces) viven en `core/ports.py`. Definen el **contrato** que el dominio necesita, pero **NO** la implementación.

**Ejemplo:**
```python
from abc import ABC, abstractmethod

class TransportistaRepositoryPort(ABC):
    @abstractmethod
    def find_by_id(self, id: int):
        pass
```

### 4. **Adaptadores en Infrastructure**

Los **Adaptadores** implementan los Puertos usando el framework:
- `infrastructure/db/repositories/` implementa `TransportistaRepositoryPort` usando el ORM de Django
- `infrastructure/api/viewsets.py` usa los repositorios para exponer la API REST

### 5. **Application Orquesta**

La capa `application/` contiene los **Casos de Uso** que:
- Reciben peticiones de la infraestructura (ej. un ViewSet)
- Llaman a los Puertos (interfaces) para obtener datos
- Ejecutan lógica de negocio del `core/`
- Retornan resultados

---

## 📋 Flujo de Datos Típico

```
1. Cliente HTTP → infrastructure/api/viewsets.py
2. ViewSet → application/use_cases/crear_transportista.py
3. Caso de Uso → core/ports.py (TransportistaRepositoryPort)
4. Infrastructure/db/repositories/ → Implementa el puerto usando Django ORM
5. Respuesta fluye de vuelta: Infrastructure → Application → Core → Application → Infrastructure → Cliente
```

---

## ✅ Checklist de Validación

Antes de hacer commit, verifica:

- [ ] ¿El código en `core/` importa Django? → **VIOLACIÓN**
- [ ] ¿El código en `application/` importa directamente de `infrastructure/`? → **VIOLACIÓN**
- [ ] ¿Los modelos de Django están en `infrastructure/db/models.py`? → ✅
- [ ] ¿Los Puertos están en `core/ports.py`? → ✅
- [ ] ¿Los repositorios implementan los Puertos? → ✅

---

## 🎯 Objetivo Final

Esta arquitectura garantiza:
- **Testabilidad:** El `core/` se puede probar sin Django
- **Mantenibilidad:** Cambios en el framework no afectan el dominio
- **Escalabilidad:** Fácil cambiar de Django a otro framework si es necesario
- **Claridad:** Separación clara de responsabilidades

---

**Última actualización:** Definido por el Arquitecto de Sistema (Agente 1)

