# 🔧 Solución de Problemas - Frontend SIGOT

## Error: `ERR_CONNECTION_REFUSED`

### Síntoma
```
POST http://localhost:8000/api/auth/register/ net::ERR_CONNECTION_REFUSED
POST http://localhost:8000/api/auth/login/ net::ERR_CONNECTION_REFUSED
```

### Causa
El backend Django no está corriendo en el puerto 8000.

### Solución

1. **Verifica que el backend esté corriendo:**
   ```bash
   # En la raíz del proyecto (donde está manage.py)
   python manage.py runserver
   ```

2. **Verifica que el servidor responda:**
   - Abre http://localhost:8000/api/ en tu navegador
   - Deberías ver una respuesta (aunque sea un 404)

3. **Si el backend no inicia:**
   - Revisa `BACKEND_SETUP.md` en la raíz del proyecto
   - Asegúrate de tener PostgreSQL corriendo
   - Ejecuta las migraciones: `python manage.py migrate`

---

## Error: CORS bloqueado

### Síntoma
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

### Solución

1. **Verifica que `django-cors-headers` esté instalado:**
   ```bash
   pip install django-cors-headers
   ```

2. **Verifica la configuración en `sigot/boot/settings.py`:**
   - Debe tener `'corsheaders'` en `INSTALLED_APPS`
   - Debe tener `'corsheaders.middleware.CorsMiddleware'` en `MIDDLEWARE`
   - Debe tener `CORS_ALLOWED_ORIGINS` configurado

3. **Reinicia el servidor Django**

---

## Error: MetaMask (Puede ignorarse)

### Síntoma
```
Uncaught (in promise) i: Failed to connect to MetaMask
```

### Causa
Es un error de la extensión MetaMask del navegador, no afecta a SIGOT.

### Solución
Puedes ignorarlo completamente. Si te molesta, desactiva la extensión MetaMask temporalmente.

---

## Error: Token no válido / 401 Unauthorized

### Síntoma
Después de iniciar sesión, las peticiones fallan con 401.

### Solución

1. **Verifica que el token se guarde en localStorage:**
   - Abre DevTools → Application → Local Storage
   - Debe haber `auth_token` y `auth_user`

2. **Limpia localStorage y vuelve a iniciar sesión:**
   ```javascript
   // En la consola del navegador
   localStorage.clear()
   ```

3. **Verifica que el backend esté usando JWT correctamente**

---

## El frontend no se conecta al backend

### Checklist

- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Frontend corriendo en `http://localhost:3000`
- [ ] CORS configurado en Django
- [ ] No hay errores en la consola del backend
- [ ] Las rutas de la API coinciden con `openapi.yml`

### Verificar conexión

Abre la consola del navegador (F12) y ejecuta:

```javascript
fetch('http://localhost:8000/api/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Si ves un error, el backend no está accesible.

---

## Problemas de instalación

### Error: `npm install` falla

```bash
# Limpia la caché
npm cache clean --force

# Elimina node_modules y reinstala
rm -rf node_modules package-lock.json
npm install
```

### Error: TypeScript no encuentra módulos

```bash
# Reinstala dependencias
npm install

# Verifica tsconfig.json
# Asegúrate de que "baseUrl" y "paths" estén configurados
```

---

## Más Ayuda

- **Backend:** Revisa `BACKEND_SETUP.md` en la raíz del proyecto
- **API:** Consulta `openapi.yml` para ver los endpoints disponibles
- **Logs:** Revisa la consola del navegador (F12) y los logs del servidor Django


