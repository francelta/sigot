"""
Permisos personalizados para la API
"""

from rest_framework import permissions


class IsTransportista(permissions.BasePermission):
    """
    Permiso que verifica que el usuario autenticado es un transportista.
    Un usuario es transportista si tiene un objeto Transportista relacionado.
    """

    def has_permission(self, request, view):
        """
        Verifica que el usuario autenticado es transportista.
        """
        if not request.user or not request.user.is_authenticated:
            return False

        # Un usuario es transportista si tiene un objeto Transportista relacionado
        return hasattr(request.user, 'transportista')


