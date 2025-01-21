from django.urls import reverse, NoReverseMatch
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.apps import apps
from .models import *
import urllib.parse  # Import urllib.parse for URL decoding
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from .models import ActionLog
import json
from django.utils.timezone import now
from django.db.models import Q
import logging
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ObjectDoesNotExist




class MultiFieldFilterMixin:
    """
    Универсальный миксин для фильтрации записей по указанным полям.
    """
    filter_fields = []  # Поля для частичного поиска
    exact_filter_fields = []  # Поля для точного поиска

    def filter_by_fields(self, request):
        filters = Q()  # Используем Q для сложных фильтров

        # Частичный поиск
        for field in self.filter_fields:
            value = request.query_params.get(field, '').strip()
            if value:
                filters |= Q(**{f"{field}__iregex": value})

        # Точный поиск
        for field in self.exact_filter_fields:
            value = request.query_params.get(field, '').strip()
            if value:
                filters &= Q(**{field: value})  # Точный фильтр

        queryset = self.get_queryset()

        if filters:
            queryset = queryset.filter(filters)

        return queryset



class AuditLogMixin:
    """
    Миксин для автоматического логирования действий пользователя.
    """

    def log_action(self, user, obj=None, description=None, action_user=None):
        """
        Логирует действие пользователя.
        """
        content_type = ContentType.objects.get_for_model(obj) if obj else None
        object_id = obj.id if obj else None
        UserActionLog.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            description=description,
            action_user=action_user
        )

    def log_action_from_request(self, obj=None, description=None, action_user=None):
        """
        Упрощенный метод для логирования действия с текущим пользователем из запроса.
        """
        self.log_action(self.request.user, obj, description, action_user)

    def perform_update(self, serializer):
        """
        Логирование обновления объекта с фиксацией изменений.
        """
        obj = self.get_object()
        updated_obj = serializer.save()
        self.log_action_from_request(
            updated_obj,
            f"Обновлен объект {updated_obj}",
            action_user=f"Пользователь id={self.request.user.id} обновил объект id={updated_obj.id}"
        )
        return updated_obj

    def perform_create(self, serializer):
        """
        Логирование создания объекта.
        """
        obj = serializer.save()
        self.log_action_from_request(
            obj,
            f"Создан объект {obj}",
            action_user=f"Пользователь id={self.request.user.id} создал объект id={obj.id}"
        )
        return obj

    def perform_destroy(self, instance):
        """
        Логирование удаления объекта.
        """
        self.log_action_from_request(
            instance,
            f"Удален объект {instance}",
            action_user=f"Пользователь id={self.request.user.id} удалил объект id={instance.id}"
        )
        super().perform_destroy(instance)






# для фильтрации регистронезависимого поиска с помощью регуляных выражений
class FilterByKeywordMixin:
    """
    Миксин для фильтрации записей по ключевым словам.
    """
    search_fields = []  # Определите поля для поиска в каждом ViewSet

    def filter_by_keyword(self, request):
        query = request.query_params.get('query', '').strip()
        if not query:
            return Response({"error": "Query parameter 'query' is required."}, status=400)

        terms = query.split(' ')  # Разбиваем запрос на термины
        queryset = self.get_queryset()
        q_objects = Q()  # Создаем объект Q для построения сложных запросов

        # Построение запросов
        for term in terms:
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__iregex': term})  # Используем iregex для частичного поиска

        results = queryset.filter(q_objects).distinct()  # distinct() исключает дубликаты
        page = self.paginate_queryset(results)  # Применяем пагинацию

        if page is not None:  # Возвращаем пагинированный ответ
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если пагинация не требуется
        serializer = self.get_serializer(results, many=True)
        return Response({'results': serializer.data})


# миксин для сохранения любого набора данных в excel формат
# http://myapi.com/currateapi/?export_to_excel=True
# ?format=excel - добавка для получения данных в формате excel
class ExcelExportMixin:
    def export_data_to_excel(self, queryset):
        # Создаем DataFrame из queryset
        df = pd.DataFrame.from_records(queryset.values())

        # Создаем объект HttpResponse с правильным заголовком Content-Disposition
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=export.xls'
        # Записываем DataFrame в Excel файл
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer)

        return response


# миксин для сортировки
class SortingMixin:
    # данные параметры можно переопределить в определенной вьюшке
    default_sort_field = 'id'
    default_sort_direction = 'desc'
    paginate_by = 50

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', self.default_sort_field)
        sort_direction = self.request.GET.get('direction', self.default_sort_direction)
        return super().get_queryset().order_by(f'{"-" if sort_direction == "desc" else ""}{sort_field}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context

# # миксин для отображения описани свойст полей модели в формате JSON
# class ModelFieldsInfoMixin(APIView):
#     def get(self, request, *args, **kwargs):
#         current_url = request.path_info.strip('/')  # Remove leading and trailing '/'
#         url_segments = current_url.split('/')
#         # Extract the "ModelName" part without "-settings" and leading/trailing spaces
#         if len(url_segments) > 2:
#             model_name = url_segments[2].split('-')[0].strip()  # Remove leading/trailing spaces
#         else:
#             # Handle the case where there are not enough segments
#             pass
#         try:
#             model = apps.get_model('Buh', model_name=model_name)
#         except LookupError:
#             return Response({"error": f"Model '{model_name}' not found."}, status=404)
#         model_fields = model._meta.fields
#         fields_info = {}
#         for field in model_fields:
#             field_info = {
#                 "name": field.name,
#                 "verbose_name": field.verbose_name,
#                 "blank": not field.blank,
#                 "null": not field.null,
#                 "max_length": field.max_length if hasattr(field, 'max_length') else None,
#                 "type": field.__class__.__name__
#             }
#             fields_info[field.name] = field_info
#
#         model_info = {
#             "model_name": model_name,
#             "fields": fields_info
#         }
#
#         return Response(model_info)


# class LoggableMixin:
#     """
#     Миксин для автоматического логирования действий над объектами.
#     """
#
#     def save(self, *args, **kwargs):
#         from core.models import ActionLog  # Оставляем импорт внутри метода
#
#         is_update = self.pk is not None
#         user = kwargs.pop('user', None)
#
#         before_state = model_to_dict(self) if is_update else None
#
#         super().save(*args, **kwargs)
#
#         after_state = model_to_dict(self)
#
#         if user:
#             ActionLog.objects.create(
#                 user=user,
#                 content_type=ContentType.objects.get_for_model(self),
#                 object_id=self.pk,
#                 action='UPDATE' if is_update else 'CREATE',
#                 before_state=json.dumps(before_state, default=str) if before_state else None,
#                 after_state=json.dumps(after_state, default=str),
#             )
#
#     def delete(self, *args, **kwargs):
#         from core.models import ActionLog  # Оставляем импорт внутри метода
#
#         user = kwargs.pop('user', None)
#         before_state = model_to_dict(self)
#
#         object_id = self.pk
#         super().delete(*args, **kwargs)
#
#         if user:
#             ActionLog.objects.create(
#                 user=user,
#                 content_type=ContentType.objects.get_for_model(self),
#                 object_id=object_id,
#                 action='DELETE',
#                 before_state=json.dumps(before_state, default=str),
#                 after_state=None,
#             )