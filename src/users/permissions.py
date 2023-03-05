from rest_framework.permissions import BasePermission

from users.constants import Role
from users.models import User


class RoleIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


class AccountOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.USER

    def has_object_permission(self, request, view, obj: User):
        return obj.password == request.user.make_password(request["password"])
