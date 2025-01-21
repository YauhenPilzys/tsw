from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений, который позволяет только администраторам редактировать объекты.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # методы, которые не изменяют данные
            return True
        else:
            return request.user.is_staff  # пользователь админ
