# 🗺️ Configuración del Mapa (Leaflet + OpenStreetMap)

El mapa utiliza **Leaflet** con **OpenStreetMap**, que es **completamente gratuito** y no requiere configuración de API keys.

## ✅ Sin Configuración Necesaria

A diferencia de Mapbox, Leaflet con OpenStreetMap:
- ✅ **No requiere API key**
- ✅ **Completamente gratuito**
- ✅ **Sin límites de uso**
- ✅ **Open source**

## Características

- **Mapa base**: OpenStreetMap (gratuito)
- **Marcadores personalizados**: Círculos de colores para transportistas
- **Geolocalización**: Obtiene automáticamente la ubicación del usuario
- **Controles**: Zoom y navegación incluidos

## Personalización (Opcional)

Si quieres cambiar el estilo del mapa, puedes usar otros proveedores de tiles gratuitos:

### Opciones de Tiles Gratuitos

1. **OpenStreetMap** (por defecto):
   ```javascript
   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; OpenStreetMap contributors'
   })
   ```

2. **CartoDB Positron** (estilo claro):
   ```javascript
   L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
     attribution: '&copy; OpenStreetMap & CartoDB'
   })
   ```

3. **Stamen Terrain**:
   ```javascript
   L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.png', {
     attribution: '&copy; Stamen Design & OpenStreetMap'
   })
   ```

Para cambiar el proveedor, edita `frontend/src/composables/useMap.ts` en la función `initMap()`.

## Solución de Problemas

### El mapa no se muestra

1. Verifica que `leaflet` esté instalado: `npm install`
2. Verifica que el CSS de Leaflet esté importado en `style.css`
3. Revisa la consola del navegador para errores

### Los iconos de marcadores no se ven

Los iconos de Leaflet a veces tienen problemas con bundlers. El código ya incluye un fix para esto en `useMap.ts`. Si aún hay problemas, verifica que los archivos de iconos estén en `node_modules/leaflet/dist/images/`.

### El mapa está en blanco

- Verifica tu conexión a internet (OpenStreetMap requiere conexión)
- Revisa la consola del navegador para errores de CORS o red


