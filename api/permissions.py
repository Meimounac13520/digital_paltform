from rest_framework import permissions
# Permissions personnalisées
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.name == 'Admin'

class IsDirectorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role and request.user.role.name == 'Directeur'

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.name == 'Agent'

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow full access to admins, read‑only to others."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsSameAgencyOrAdmin(permissions.BasePermission):
    """Object‑level permission to restrict access to same agency (or admin)."""
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # most objects have an `agency` FK
        return getattr(obj, 'agency_id', None) == getattr(request.user, 'agency_id', None)