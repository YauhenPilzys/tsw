from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from .models import ActionLog


class ActionLogMiddleware:
    """
    Middleware для автоматического логирования действий пользователей.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Обрабатываем запрос до выполнения View
        response = self.get_response(request)

        # Логируем действия после обработки View
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Определяем модель и объект, если возможно
            content_type = None
            object_id = None

            # Записываем лог
            ActionLog.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                action=f"{request.method} {request.path}",
                before_state=None,
                after_state=None,
                datetime=now()
            )

        return response