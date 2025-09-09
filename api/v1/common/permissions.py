from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser and request.user.role == "admin"

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor and request.user.role == "doctor"

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_receptionist and request.user.role == "receptionist"
