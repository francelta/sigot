# 🤝 Guía de Contribución - ConnecMaq

¡Gracias por tu interés en contribuir a **ConnecMaq**! Esta guía te ayudará a empezar.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#-código-de-conducta)
- [¿Cómo Puedo Contribuir?](#-cómo-puedo-contribuir)
- [Configuración del Entorno](#-configuración-del-entorno)
- [Proceso de Desarrollo](#-proceso-de-desarrollo)
- [Guía de Estilo](#-guía-de-estilo)
- [Proceso de Pull Request](#-proceso-de-pull-request)

---

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

**En resumen:**
- 🤝 Sé respetuoso y profesional
- 💬 Usa lenguaje inclusivo
- 🎯 Céntrate en lo mejor para el proyecto
- ❤️ Acepta críticas constructivas con gracia

---

## 🎯 ¿Cómo Puedo Contribuir?

### Reportar Bugs

Si encuentras un bug:

1. **Busca primero** en los [Issues existentes](https://github.com/francelta/sigot/issues)
2. Si no existe, **crea un nuevo Issue** con:
   - Título descriptivo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si es aplicable
   - Información del sistema (OS, Python version, etc.)

**Template de Bug Report:**
```markdown
**Descripción:**
Descripción clara del bug

**Pasos para reproducir:**
1. Ir a '...'
2. Click en '...'
3. Ver error

**Comportamiento esperado:**
Lo que debería pasar

**Screenshots:**
Si aplica

**Entorno:**
- OS: [ej. macOS 13.0]
- Python: [ej. 3.10.5]
- Django: [ej. 5.0.0]
```

### Sugerir Mejoras

Para sugerir nuevas características:

1. **Crea un Issue** con el tag `enhancement`
2. Describe:
   - ¿Qué problema resuelve?
   - ¿Cómo debería funcionar?
   - ¿Alternativas consideradas?

### Contribuir Código

1. **Fork** el repositorio
2. **Crea una rama** para tu feature
3. **Implementa** tu cambio
4. **Escribe tests**
5. **Envía** un Pull Request

---

## ⚙️ Configuración del Entorno

### 1. Fork y Clonar

```bash
# Fork en GitHub, luego:
git clone https://github.com/TU-USUARIO/sigot.git
cd sigot

# Agregar upstream
git remote add upstream https://github.com/francelta/sigot.git
```

### 2. Instalar Dependencias

```bash
# Setup automático
./setup.sh

# O manual
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### 3. Crear Rama

```bash
git checkout -b feature/mi-nueva-caracteristica
```

---

## 🔄 Proceso de Desarrollo

### 1. Mantener tu Fork Actualizado

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 2. Hacer Cambios

```bash
# En tu rama de feature
git checkout feature/mi-nueva-caracteristica

# Hacer cambios...
# Editar archivos

# Verificar cambios
python manage.py check
python manage.py test

# Commit
git add .
git commit -m "feat: Agregar nueva característica X"
```

### 3. Mantener Commits Limpios

Usamos **Conventional Commits**:

```
feat: Nueva característica
fix: Corrección de bug
docs: Cambios en documentación
style: Formateo, puntos y comas, etc
refactor: Refactorización de código
test: Agregar tests
chore: Mantenimiento
```

**Ejemplos:**
```bash
git commit -m "feat: Agregar filtro de búsqueda por ciudad"
git commit -m "fix: Corregir error al subir imagen de máquina"
git commit -m "docs: Actualizar README con nueva instalación"
```

---

## 📝 Guía de Estilo

### Python (Backend)

Seguimos **PEP 8** con algunas excepciones:

```python
# Imports
import os
from django.db import models
from rest_framework import serializers

# Clases
class ProviderProfile(models.Model):
    """Perfil de proveedor de maquinaria."""
    
    company_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Perfil de Proveedor"
        verbose_name_plural = "Perfiles de Proveedores"

# Funciones
def calculate_total_price(hours, rate):
    """
    Calcula el precio total.
    
    Args:
        hours (int): Horas de servicio
        rate (float): Tarifa por hora
    
    Returns:
        float: Precio total
    """
    return hours * rate
```

**Reglas:**
- ✅ Nombres descriptivos
- ✅ Docstrings en funciones y clases
- ✅ Type hints cuando sea útil
- ✅ Máximo 100 caracteres por línea (preferible 79)
- ✅ 2 líneas en blanco entre clases

### Django (Models, Views, Serializers)

```python
# models.py
class Machine(models.Model):
    name = models.CharField(_('name'), max_length=255)
    provider = models.ForeignKey(
        'ProviderProfile',
        on_delete=models.CASCADE,
        related_name='machines'
    )

# serializers.py
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'provider', ...]
        read_only_fields = ['id', 'created_at']

# views.py
class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

### Tests

```python
# tests.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_machine():
    """Test crear una máquina."""
    response = client.post(url, data)
    assert response.status_code == 201
    assert Machine.objects.count() == 1
```

---

## 🔍 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest api/tests/test_models.py

# Con coverage
pytest --cov=api
```

### Escribir Tests

Cada nueva característica debe incluir tests:

```python
# tests/test_machines.py
@pytest.mark.django_db
class TestMachineAPI:
    
    def test_list_machines(self, api_client):
        """Test listar máquinas."""
        url = reverse('machine-list')
        response = api_client.get(url)
        assert response.status_code == 200
    
    def test_create_machine_with_image(self, api_client, provider):
        """Test crear máquina con imagen."""
        url = reverse('machine-list')
        data = {
            'name': 'Excavadora',
            'category': 'excavator',
            'main_image': image_file
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
```

---

## 📤 Proceso de Pull Request

### 1. Antes de Enviar

**Checklist:**
- [ ] Código sigue la guía de estilo
- [ ] Tests escritos y pasando
- [ ] Documentación actualizada
- [ ] Commits son limpios y descriptivos
- [ ] No hay conflictos con `main`

### 2. Crear Pull Request

```bash
# Push a tu fork
git push origin feature/mi-nueva-caracteristica
```

Luego en GitHub:

1. Ve a tu fork
2. Click en "Pull Request"
3. Llena la plantilla:

**Template de PR:**
```markdown
## Descripción
Breve descripción de los cambios

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva característica
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
Describe cómo probaste tus cambios

## Checklist
- [ ] Mi código sigue la guía de estilo
- [ ] He hecho self-review
- [ ] He comentado código complejo
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan warnings
- [ ] He agregado tests
- [ ] Tests nuevos y existentes pasan
```

### 3. Code Review

- Responde a comentarios
- Haz cambios solicitados
- Push actualizaciones a la misma rama

### 4. Merge

Una vez aprobado:
- El maintainer hará merge
- Tu rama será cerrada
- ¡Celebra! 🎉

---

## 🎨 Áreas de Contribución

### Backend (Django)
- 🔧 Mejoras en la API
- 🔐 Seguridad
- ⚡ Performance
- 🧪 Tests

### Frontend (Vue.js) - Próximamente
- 🎨 UI/UX
- 📱 Responsive design
- ♿ Accesibilidad

### Documentación
- 📝 Mejorar README
- 📚 Tutoriales
- 🌍 Traducciones

### DevOps
- 🐳 Docker
- 🚀 CI/CD
- ☁️ Deploy

---

## 💡 Ideas de Contribución

### Good First Issues

Busca issues con el tag `good first issue`:
- Correcciones de typos
- Mejorar mensajes de error
- Agregar validaciones simples
- Documentación

### Features Necesarias

- [ ] Sistema de notificaciones
- [ ] Búsqueda avanzada con filtros
- [ ] Geolocalización
- [ ] Sistema de valoraciones
- [ ] Integración de pagos
- [ ] App móvil

---

## 📞 Contacto

- **Issues:** https://github.com/francelta/sigot/issues
- **Email:** [Tu email si quieres agregarlo]
- **Discussions:** [Si habilitas GitHub Discussions]

---

## 🙏 Reconocimientos

Todos los contribuidores serán reconocidos en:
- README.md
- CONTRIBUTORS.md (próximamente)

---

**¡Gracias por contribuir a ConnecMaq!** 🚀

Tu tiempo y esfuerzo ayudan a hacer este proyecto mejor para todos. 💙

