from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los dueños de un objeto puedan editarlo.
    """

    def has_object_permission(self, request, view, obj):
        # Los permisos de lectura (GET, HEAD, OPTIONS) se permiten a cualquiera.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Los permisos de escritura (PUT, DELETE) solo se permiten al dueño del snippet.
        return obj.owner == request.user