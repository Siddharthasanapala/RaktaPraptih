from rest_framework.permissions import BasePermission , SAFE_METHODS

class IsDonor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'donor')

class IsBloodBank(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'bloodbank')