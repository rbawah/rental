from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow managers to edit home, units and buildings.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.manager == request.user