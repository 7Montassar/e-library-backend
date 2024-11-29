from rest_framework import permissions

class IsAuthenticatedAndReadOnly(permissions.BasePermission):
    """
    Allow read-only access for authenticated users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS


class IsVisitorAndCanAdd(permissions.BasePermission):
    """
    Allow visitors to add books.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role == 'visitor' 
            and request.method == 'POST'
        )


class IsAdminAndCanPerformAll(permissions.BasePermission):
    """
    Allow admin users to perform all actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
