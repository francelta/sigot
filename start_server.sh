#!/bin/bash
# Script para iniciar el servidor Django con soporte WebSocket usando Daphne

echo "🚀 Iniciando servidor Django con Daphne (soporte WebSocket)..."
echo "📡 El servidor estará disponible en: http://localhost:8000"
echo "🔌 WebSockets disponibles en: ws://localhost:8000/ws/"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

daphne -b 0.0.0.0 -p 8000 sigot.boot.asgi:application

