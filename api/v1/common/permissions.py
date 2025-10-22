from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_hospital_staff
