# ✅ Solución: Error CORS

## 🐛 El Problema

```
Access to XMLHttpRequest at 'http://localhost:8000/api/users/' from origin 
'http://localhost:5176' has been blocked by CORS policy: Response to preflight 
request doesn't pass access control check: No 'Access-Control-Allow-Origin' 
header is present on the requested resource.
```

## 🔍 ¿Qué es CORS?

**CORS** (Cross-Origin Resource Sharing) es un mecanismo de seguridad del navegador que:

1. **Protege** contra peticiones no autorizadas entre diferentes orígenes
2. **Bloquea** peticiones cuando:
   - El dominio es diferente (ejemplo.com vs otro.com)
   - El puerto es diferente (localhost:5176 vs localhost:8000)
   - El protocolo es diferente (http vs https)

### En tu caso:
- **Frontend:** `http://localhost:5176` ← Origen 1
- **Backend:** `http://localhost:8000` ← Origen 2
- **Resultado:** El navegador bloquea la comunicación por seguridad ❌

## ✅ La Solución

El backend Django debe **explícitamente permitir** requests desde el frontend.

### Paso 1: Actualizar CORS_ALLOWED_ORIGINS

He actualizado `backend/config/settings.py` para incluir los puertos alternativos:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Puerto por defecto de Vite
    "http://localhost:5174",  # Alternativo
    "http://localhost:5175",  # Alternativo
    "http://localhost:5176",  # ← Tu puerto actual
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:5176",
]
```

### Paso 2: Reiniciar el Backend

**IMPORTANTE:** Debes reiniciar Django para que los cambios surtan efecto.

```bash
# 1. Detén el servidor Django (Ctrl+C en la terminal del backend)

# 2. Reinicia el servidor
cd backend
source venv/bin/activate
python manage.py runserver
```

### Paso 3: Verificar

1. Asegúrate de que el backend esté corriendo
2. Recarga la página del frontend (F5)
3. Intenta registrarte de nuevo
4. ✅ Debería funcionar sin errores de CORS

---

## 🔍 ¿Por qué cambió el puerto?

Vite asigna puertos automáticamente:
- **Puerto 5173:** Puerto por defecto
- **Puerto 5174+:** Si 5173 está ocupado, usa el siguiente disponible

Esto pasa cuando:
- Tienes otra instancia de Vite corriendo
- Otro proceso usa el puerto 5173
- Reiniciaste Vite y el puerto anterior no se liberó

---

## 🎯 Verificación Rápida

### ¿El backend permite tu puerto?

1. **Abre el navegador**
2. **F12** para abrir DevTools
3. **Pestaña Network**
4. **Intenta registrarte**
5. **Busca el request a** `/api/users/`
6. **Revisa los Headers de respuesta:**
   - ✅ Debe tener: `Access-Control-Allow-Origin: http://localhost:5176`
   - ❌ Si no lo tiene: reinicia el backend

---

## 🛡️ Seguridad

### ¿Es seguro permitir múltiples orígenes?

**En desarrollo:** ✅ Sí, es seguro
- Solo localhost puede acceder
- Los puertos están en tu máquina local

**En producción:** ⚠️ Debes cambiar esto
- Solo permite tu dominio real
- Ejemplo: `["https://tuapp.com"]`

### Configuración para producción:

```python
# En production (cambiar en settings.py)
if DEBUG:
    # Desarrollo: múltiples puertos localhost
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:5174",
        # ...
    ]
else:
    # Producción: solo tu dominio
    CORS_ALLOWED_ORIGINS = [
        "https://tudominio.com",
        "https://www.tudominio.com",
    ]
```

---

## 📋 Checklist de Solución

- [x] ✅ Actualicé CORS_ALLOWED_ORIGINS en settings.py
- [ ] ⏳ Reinicia el backend Django
- [ ] ⏳ Recarga el frontend (F5)
- [ ] ⏳ Prueba el registro/login nuevamente
- [ ] ✅ Verifica que no hay más errores de CORS

---

## 🔄 Alternativa: Usar puerto 5173

Si prefieres usar siempre el mismo puerto (5173):

```bash
# Mata cualquier proceso en el puerto 5173
lsof -ti:5173 | xargs kill -9

# Inicia Vite normalmente
npm run dev
```

Esto asegura que siempre uses el puerto 5173 configurado originalmente.

---

## 🆘 Si Aún No Funciona

### 1. Verifica que el backend está corriendo:
```bash
curl http://localhost:8000/api/
```

Debería responder sin errores.

### 2. Verifica CORS en Django:
```bash
cd backend
python manage.py shell
```

Luego ejecuta:
```python
from django.conf import settings
print(settings.CORS_ALLOWED_ORIGINS)
```

Debería mostrar la lista con tu puerto.

### 3. Verifica que django-cors-headers está instalado:
```bash
pip list | grep django-cors-headers
```

Debería mostrar: `django-cors-headers  4.3.1` (o similar)

### 4. Limpia caché del navegador:
- Chrome/Edge: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete
- Safari: Cmd+Alt+E

---

**¡Problema resuelto! 🎉**

Después de reiniciar Django, el frontend debería comunicarse sin problemas con el backend.

