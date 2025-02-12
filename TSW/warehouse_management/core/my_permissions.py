from rest_framework import permissions


class IsWarehouseUserWithDeleteAccess(permissions.BasePermission):
    """
    Разрешает создание и редактирование записей всем пользователям СВХ (is_wh_user=True).
    Удалять записи могут только старшие администраторы (is_main_admin=True).
    """

    def has_permission(self, request, view):
        # Разрешаем доступ ко всем операциям, если пользователь работает на СВХ
        return getattr(request.user, 'is_wh_user', False)

    def has_object_permission(self, request, view, obj):
        # Разрешаем редактирование (PATCH, PUT) всем пользователям СВХ
        if request.method in ["PATCH", "PUT"]:
            return getattr(request.user, 'is_wh_user', False)

        #Удаление разрешено только старшим администраторам (`is_main_admin=True`)
        if request.method == "DELETE":
            return getattr(request.user, 'is_main_admin', False) is False  # Только `is_main_admin=True` может удалять

        # Разрешаем чтение всем пользователям СВХ
        return True