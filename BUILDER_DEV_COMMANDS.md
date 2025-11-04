# 🛠️ Builder.io Dev Commands - ConnecMaq

## 🎯 Comandos de Desarrollo Rápido

Script interactivo para facilitar el desarrollo con Builder.io.

---

## 🚀 Uso

### Modo Interactivo (Menú)

**Unix/Mac/Linux:**
```bash
./dev-builder.sh
```

**Windows:**
```batch
dev-builder.bat
```

**Con Make:**
```bash
make builder-dev
```

### Modo Comando Directo

**Unix/Mac/Linux:**
```bash
./dev-builder.sh [comando]
```

**Ejemplos:**
```bash
./dev-builder.sh status    # Ver estado
./dev-builder.sh check     # Verificar API keys
./dev-builder.sh test      # Test de integración
./dev-builder.sh help      # Ayuda rápida
```

**Con Make:**
```bash
make builder-status    # Ver estado
make builder-check     # Verificar API keys
make builder-test      # Test de integración
```

---

## 📋 Comandos Disponibles

### 1️⃣ Status - Ver Estado

```bash
./dev-builder.sh status
# o
make builder-status
```

**Qué hace:**
- ✅ Verifica estructura de archivos
- ✅ Verifica variables de entorno
- ✅ Verifica backend Django
- ✅ Muestra si todo está configurado correctamente

**Salida esperada:**
```
============================================
  Estado de Builder.io
============================================

Estructura de archivos:
✓ builder-config/ existe
✓ builder.config.json
✓ README.md
✓ webhooks/
✓ templates/

Variables de entorno:
✓ BUILDER_IO_API_KEY configurado
✓ BUILDER_IO_PRIVATE_KEY configurado

Backend Django:
✓ Python 3 instalado
✓ Django project encontrado
```

---

### 2️⃣ Check - Verificar Conectividad

```bash
./dev-builder.sh check
# o
make builder-check
```

**Qué hace:**
- ✅ Verifica que API Key esté configurado
- ✅ Test de conexión con Builder.io API
- ✅ Confirma que el API Key funciona

**Salida esperada:**
```
============================================
  Verificación de Builder.io
============================================

→ Verificando conectividad con Builder.io...
✓ Conexión exitosa con Builder.io API
→ API Key válido y funcionando
```

---

### 3️⃣ Config - Ver Configuración

```bash
./dev-builder.sh config
```

**Qué hace:**
- ✅ Muestra API Keys (parcialmente ocultos)
- ✅ Muestra modelos configurados
- ✅ Muestra configuración actual

**Salida esperada:**
```
============================================
  Configuración de Builder.io
============================================

API Keys:
  BUILDER_IO_API_KEY: bpk-1234567890abcd... (oculto)
  BUILDER_IO_PRIVATE_KEY: pvk-abcdef123456... (oculto)
  BUILDER_IO_SPACE_ID: abc123def456

Modelos configurados:
  "name": "page"
  "name": "landing-page"
  "name": "blog-post"
```

---

### 4️⃣ Preview - Configurar Preview Local

```bash
./dev-builder.sh preview
```

**Qué hace:**
- ✅ Muestra instrucciones para configurar preview local
- ✅ Explica cómo conectar Builder.io editor con tu servidor local

**Instrucciones:**
```
============================================
  Preview URL Local
============================================

Para usar preview local en Builder.io:

1. Inicia tu servidor Django:
   cd backend
   python manage.py runserver

2. En Builder.io editor:
   Settings (⚙️) → Preview URLs

3. Agrega estas URLs:
   http://localhost:8000
   http://127.0.0.1:8000

4. Ahora puedes hacer preview en tiempo real
```

---

### 5️⃣ Models - Listar Modelos

```bash
./dev-builder.sh models
```

**Qué hace:**
- ✅ Lista todos los modelos de contenido configurados
- ✅ Muestra detalles de cada modelo

**Salida esperada:**
```
============================================
  Modelos de Builder.io
============================================

Modelos disponibles:

  "name": "page",
  "kind": "page",
  "description": "Páginas del sitio",

  "name": "landing-page",
  "kind": "page",
  "description": "Landing pages de marketing",

  "name": "blog-post",
  "kind": "data",
  "description": "Posts del blog",
```

---

### 6️⃣ Test - Test de Integración

```bash
./dev-builder.sh test
# o
make builder-test
```

**Qué hace:**
- ✅ Test de API de Builder.io
- ✅ Test de modelos configurados
- ✅ Test de webhook endpoint
- ✅ Verifica que todo funcione

**Salida esperada:**
```
============================================
  Test de Integración
============================================

Test 1: Listar contenido del modelo 'page'
✓ API responde correctamente
→ Contenido encontrado en modelo 'page'

Test 2: Verificar acceso a modelos
✓ Modelos configurados localmente

Test 3: Verificar webhook endpoint
✓ Webhook endpoint configurado en Django

✓ Tests completados
```

---

### 7️⃣ Docs - Ver Documentación

```bash
./dev-builder.sh docs
```

**Qué hace:**
- ✅ Abre la documentación local completa
- ✅ Muestra el README de Builder.io

---

### 8️⃣ Help - Ayuda Rápida

```bash
./dev-builder.sh help
```

**Qué hace:**
- ✅ Muestra ayuda rápida
- ✅ Primeros pasos
- ✅ Comandos útiles
- ✅ Recursos

---

### 9️⃣ Logs - Ver Logs

```bash
./dev-builder.sh logs
```

**Qué hace:**
- ✅ Muestra logs de webhooks de Builder.io
- ✅ Útil para debugging

---

### 🔟 Clean - Limpiar Cache

```bash
./dev-builder.sh clean
```

**Qué hace:**
- ✅ Limpia archivos `__pycache__`
- ✅ Limpia archivos `*.pyc`
- ✅ Limpia cache temporal

---

## 💡 Casos de Uso

### 📌 Caso 1: Verificar que todo está configurado

```bash
# Ver estado general
./dev-builder.sh status

# Si hay errores, verificar conectividad
./dev-builder.sh check

# Ver configuración actual
./dev-builder.sh config
```

### 📌 Caso 2: Configurar preview local

```bash
# Ver instrucciones
./dev-builder.sh preview

# En otra terminal, ejecutar Django
cd backend
python manage.py runserver
```

### 📌 Caso 3: Debugging

```bash
# Ver estado
./dev-builder.sh status

# Test de integración
./dev-builder.sh test

# Ver logs
./dev-builder.sh logs
```

### 📌 Caso 4: Primeros pasos

```bash
# Ver ayuda
./dev-builder.sh help

# Ver documentación completa
./dev-builder.sh docs

# Verificar configuración
./dev-builder.sh check
```

---

## 🔧 Comandos Make Disponibles

```bash
make builder-dev        # Abrir menú interactivo
make builder-status     # Ver estado
make builder-check      # Verificar API keys
make builder-test       # Test de integración
make builder-docs       # Ver documentación
```

---

## 📊 Flujo de Trabajo Típico

### 1️⃣ Al Empezar el Día

```bash
# Verificar estado
make builder-status

# Verificar conectividad
make builder-check

# Ejecutar backend
make run  # o cd backend && python manage.py runserver
```

### 2️⃣ Desarrollo Activo

```bash
# Menú interactivo para acceso rápido
make builder-dev

# O comandos directos
./dev-builder.sh preview   # Para configurar preview
./dev-builder.sh models    # Para ver modelos
./dev-builder.sh test      # Para probar cambios
```

### 3️⃣ Debugging

```bash
# Ver logs
./dev-builder.sh logs

# Test de integración
./dev-builder.sh test

# Limpiar cache
./dev-builder.sh clean
```

---

## 🎯 Tips

### ✅ Usar en conjunto con otros comandos

```bash
# Ver estado de Builder.io
./dev-builder.sh status

# Ejecutar backend
make run

# Ejecutar tests
make test
```

### ✅ Atajos rápidos

Agrega a tu `~/.bashrc` o `~/.zshrc`:

```bash
alias bdev='./dev-builder.sh'
alias bstatus='./dev-builder.sh status'
alias bcheck='./dev-builder.sh check'
alias btest='./dev-builder.sh test'
```

Luego:
```bash
bstatus    # En vez de ./dev-builder.sh status
bcheck     # En vez de ./dev-builder.sh check
btest      # En vez de ./dev-builder.sh test
```

---

## 🐛 Troubleshooting

### Error: "Builder.io no está configurado"

**Solución:**
```bash
# Ejecutar setup primero
./setup-builder.sh
# o
make setup-builder
```

### Error: "API Key no configurado"

**Solución:**
```bash
# Editar backend/.env
nano backend/.env

# Agregar:
BUILDER_IO_API_KEY=tu-api-key-aqui
BUILDER_IO_PRIVATE_KEY=tu-private-key-aqui
```

### Error: "Conexión fallida"

**Solución:**
```bash
# Verificar API key
./dev-builder.sh config

# Verificar conectividad
./dev-builder.sh check

# Verificar en Builder.io que el API key sea válido
```

---

## 📚 Recursos

- **Setup:** [BUILDER_IO_SETUP.md](BUILDER_IO_SETUP.md)
- **Documentación Local:** `builder-config/README.md`
- **Docs Online:** https://www.builder.io/c/docs
- **API Docs:** https://www.builder.io/c/docs/api

---

## 🎊 Resumen

Los **dev commands** facilitan el trabajo diario con Builder.io:

✅ **Verificación rápida** de configuración
✅ **Test automático** de integración
✅ **Preview local** configuración fácil
✅ **Debugging** con logs y status
✅ **Modo interactivo** con menú visual

**Para empezar:**
```bash
./dev-builder.sh
```

¡Selecciona una opción del menú y comienza a desarrollar! 🚀

