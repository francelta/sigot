"""
URLs principales de SIGOT
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'SIGOT Backend API',
        'endpoints': {
            'api': '/api/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', health_check, name='root'),
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include(('sigot.infrastructure.api.urls', 'api'), namespace='api')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

