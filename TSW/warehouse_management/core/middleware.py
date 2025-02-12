import json
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import *

class RequestLoggingMiddleware:
    """
    Middleware для автоматического логирования всех запросов.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем информацию о пользователе
        user = request.user if request.user.is_authenticated else None

        # Сохраняем информацию о запросе
        action = request.method.lower()  # get, post, put, delete
        path = request.path
        body_data = None

        # Логируем тело запроса только если это POST, PUT или DELETE
        if request.method in ["POST", "PUT", "DELETE"]:
            try:
                body_data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                body_data = request.body.decode("utf-8")

        # Создаем запись в логах перед выполнением запроса
        log_entry = UserActionLog.objects.create(
            user=user,
            action=action,
            content_type=None,
            object_id=None,
            description=f"Запрос {request.method} {path}",
            action_user=f"Пользователь id={user.id} сделал запрос {request.method} {path}" if user else f"Анонимный пользователь сделал запрос {request.method} {path}",
            datetime=now()
        )

        # Выполняем сам запрос
        response = self.get_response(request)

        # Логируем статус ответа
        log_entry.description += f" | Статус: {response.status_code}"
        log_entry.save()

        return response

    def process_exception(self, request, exception):
        """Логирует ошибки в запросах"""
        user = request.user if request.user.is_authenticated else None
        path = request.path

        UserActionLog.objects.create(
            user=user,
            action="error",
            content_type=None,
            object_id=None,
            description=f"Ошибка при запросе {request.method} {path}: {exception}",
            action_user=f"Пользователь id={user.id} вызвал ошибку {exception}" if user else f"Анонимный пользователь вызвал ошибку {exception}",
            datetime=now()
        )

        return JsonResponse({"error": "Произошла ошибка на сервере"}, status=500)