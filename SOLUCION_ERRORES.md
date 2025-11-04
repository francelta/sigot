# 🐛 Solución de Errores Comunes

## Error 401: Unauthorized (Login)

### ❌ Error:
```
Failed to load resource: the server responded with a status of 401 (Unauthorized)
Endpoint: /api/token/
```

### 🔍 ¿Qué significa?
El servidor rechazó tus credenciales de login porque:
- El email no existe en la base de datos
- La contraseña es incorrecta
- No hay usuarios creados

### ✅ Solución:

**Paso 1: Verificar que tienes usuarios de prueba**
```bash
cd backend
source venv/bin/activate
python test_api.py
```

**Paso 2: Usar las credenciales correctas**

**Constructor:**
- Email: `constructor@test.com`
- Password: `TestPass123!`

**Proveedor:**
- Email: `provider@test.com`
- Password: `TestPass123!`

**Nota:** La contraseña tiene mayúscula, número y signo de exclamación.

---

## Error 400: Bad Request (Registro)

### ❌ Error:
```
Failed to load resource: the server responded with a status of 400 (Bad Request)
Endpoint: /api/users/
```

### 🔍 Causas comunes:

1. **Email ya existe**
   ```json
   { "email": ["user with this email address already exists."] }
   ```

2. **Username ya existe**
   ```json
   { "username": ["A user with that username already exists."] }
   ```

3. **Contraseñas no coinciden**
   ```json
   { "password": ["Las contraseñas no coinciden."] }
   ```

4. **Contraseña muy débil**
   ```json
   { "password": ["This password is too short. It must contain at least 8 characters."] }
   ```

5. **Falta campo requerido**
   ```json
   { "user_type": ["This field is required."] }
   ```

### ✅ Soluciones:

**Si el email ya existe:**
- Usa otro email o login con ese email

**Si la contraseña es débil:**
- Usa mínimo 8 caracteres
- Incluye mayúsculas, minúsculas y números
- Ejemplo válido: `MiPass123!`

**Si faltan campos:**
- Asegúrate de seleccionar Constructor o Proveedor
- Completa todos los campos con asterisco (*)

---

## Error 400: Bad Request (Crear Máquina)

### ❌ Error:
```
Failed to load resource: the server responded with a status of 400 (Bad Request)
Endpoint: /api/machines/
```

### 🔍 Causas comunes:

1. **Falta la imagen (OBLIGATORIA)**
   ```json
   { "main_image": ["This field is required."] }
   ```

2. **Imagen muy grande (>5MB)**
   ```
   Alert: La imagen no debe superar 5MB
   ```

3. **Archivo no es una imagen**
   ```json
   { "main_image": ["Upload a valid image."] }
   ```

4. **Faltan campos requeridos**
   ```json
   { "name": ["This field is required."],
     "category": ["This field is required."] }
   ```

### ✅ Soluciones:

**Para la imagen:**
```javascript
// El formulario ya valida, pero asegúrate de:
1. Seleccionar un archivo de imagen (JPG, PNG, GIF)
2. Que sea menor a 5MB
3. Ver el preview antes de guardar
```

**Para campos requeridos:**
- **Nombre:** Obligatorio
- **Categoría:** Obligatorio
- **Imagen:** Obligatoria (NUEVO)

---

## 🔧 Debugging: Ver Detalles del Error

### En el Frontend (Vue):

Abre la consola del navegador (F12) y busca el error completo:

```javascript
// En MachineForm.vue
catch (error) {
  console.error('Error saving machine:', error)
  console.error('Response data:', error.response?.data)  // ← Ver esto
  alert('Error al guardar maquinaria')
}
```

### Modificar temporalmente para ver el error:

```javascript
catch (error) {
  console.error('Error completo:', error)
  
  // Mostrar el error real al usuario
  const errorMsg = error.response?.data 
    ? JSON.stringify(error.response.data, null, 2)
    : 'Error desconocido'
  
  alert(`Error al guardar:\n${errorMsg}`)
}
```

---

## 🎯 Flujo de Prueba Correcto

### 1. Crear usuarios de prueba
```bash
cd backend
source venv/bin/activate
python test_api.py
```

Resultado esperado:
```
✅ Constructor creado: constructor@test.com
✅ Proveedor creado: provider@test.com
```

### 2. Login como Proveedor
```
URL: http://localhost:5176/login
Email: provider@test.com
Password: TestPass123!
```

### 3. Crear Maquinaria
```
URL: /provider/machines/new

Completar:
✅ Nombre: Excavadora Test
✅ Categoría: excavator
✅ Imagen: [Seleccionar archivo JPG/PNG < 5MB]
✅ Ver preview
✅ Guardar
```

---

## 🐛 Problemas Específicos y Soluciones

### Problema: "No puedo login"

**Checklist:**
- [ ] ¿Ejecutaste `python test_api.py`?
- [ ] ¿Usas el email correcto? (`constructor@test.com`)
- [ ] ¿Usas la password correcta? (`TestPass123!` con mayúscula)
- [ ] ¿El backend está corriendo? (puerto 8000)
- [ ] ¿El frontend está corriendo? (puerto 5176)

### Problema: "No puedo crear máquina"

**Checklist:**
- [ ] ¿Estás logueado como proveedor?
- [ ] ¿Seleccionaste una imagen?
- [ ] ¿La imagen es menor a 5MB?
- [ ] ¿Completaste nombre y categoría?
- [ ] ¿Ves el preview de la imagen?

### Problema: "Error 400 sin detalles"

**Verificar en consola del navegador:**
```javascript
// Busca en la consola (F12):
Network tab → Click en el request fallido → Response

// O en la consola:
console logs del error
```

---

## 🔍 Comandos de Verificación

### Verificar que el backend funciona:
```bash
curl http://localhost:8000/api/
```

Debe responder con un JSON.

### Verificar que hay usuarios:
```bash
cd backend
python manage.py shell

# Dentro del shell:
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.all().count())  # Debe ser > 0
print(list(User.objects.values('email')))  # Ver emails
```

### Verificar login manual:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"provider@test.com","password":"TestPass123!"}'
```

Debe devolver tokens:
```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi..."
}
```

---

## 📊 Resumen de Errores HTTP

| Código | Significado | Causa Común | Solución |
|--------|-------------|-------------|----------|
| 400 | Bad Request | Datos inválidos o faltantes | Verificar campos requeridos |
| 401 | Unauthorized | Credenciales incorrectas | Verificar email/password |
| 403 | Forbidden | Sin permisos | Login como el usuario correcto |
| 404 | Not Found | Endpoint no existe | Verificar URL |
| 500 | Server Error | Error en el backend | Ver logs de Django |

---

## 🆘 Si Nada Funciona

### Reinicio Completo:

```bash
# 1. Detener todo (Ctrl+C en todas las terminales)

# 2. Backend: Recrear base de datos
cd backend
source venv/bin/activate
rm db.sqlite3
python manage.py migrate
python test_api.py

# 3. Reiniciar backend
python manage.py runserver

# 4. Frontend: Limpiar y reiniciar
cd frontend
# Limpiar caché del navegador (Ctrl+Shift+Delete)
npm run dev

# 5. Probar de nuevo
```

---

## 📝 Logs Útiles

### Ver logs del backend en tiempo real:
Los verás en la terminal donde corre Django:
```
[03/Nov/2024 10:30:00] "POST /api/token/ HTTP/1.1" 401 45
```

### Ver logs del frontend:
Abre DevTools (F12) → Console

---

**¿Necesitas ayuda con algún error específico? Copia el error completo de la consola! 🔍**

