from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import *
from .serializers import *
from .paginations import AllOtherAPIListPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .my_permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from reportlab.lib.utils import ImageReader
from urllib.parse import quote
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import re
from django.contrib.contenttypes.models import ContentType
from .models import ActionLog
from django.forms.models import model_to_dict
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .directory import *
from django.db.models import Q
from .mixins import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from .xml_uved import generate_xml







# Скачивание XML
# http://127.0.0.1:8000/notices/1/download_xml/
def download_notice_xml(request, notice_id):
    # Получаем объект Notice
    notice = get_object_or_404(Notice, pk=notice_id)

    # Генерируем XML
    xml_data = generate_xml(notice)

    # Формируем имя файла
    file_name = f"B_{notice.guid}-{notice.order.warehouse.customs_post}_UV.xml"

    # Возвращаем файл для скачивания
    response = HttpResponse(xml_data, content_type="application/xml")
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response




# Запрос на создание пропуска на заезд
# http://127.0.0.1:8000/pass/1/ - 1 - id logbook
def generate_pass_pdf(request, logbook_id):
    try:
        # Получение записи LogBook по ID
        logbook = LogBook.objects.select_related('place_park', 'warehouse').get(pk=logbook_id)
    except LogBook.DoesNotExist:
        return HttpResponse("Запись в журнале не найдена", status=404)

    # Абсолютный URL логотипа
    logo_url = request.build_absolute_uri(f"{settings.MEDIA_URL}images/logo.png")

    # Подготовка данных
    context = {
        "logbook": logbook,
        "rules": [
            "проносить на территорию товары, которые могут нанести ущерб здоровью либо товарам, хранящимся на СВХ (оружие, боеприпасы, взрывчатые, отравляющие вещества, горючие и легковоспламеняющиеся материалы, спиртные напитки и т.д.);",
            "курить, справлять естественные надобности вне установленных мест;",
            "пользоваться открытым огнем с целью разогрева пищи и в иных случаях;",
            "приносить, распивать спиртные напитки, употреблять психотропные и наркотические вещества;",
            "выбрасывать мусор, пищевые отходы вне специально отведённых для этих целей мест;",
            "производить техническое обслуживание, ремонт и мойку транспортных средств, иные виды работ, которые могут привести к порче асфальтированного покрытия и нанесению физического вреда водителю (иным лицам);",
            "допускать вытекание горюче-смазочных материалов из автомобиля;",
            "управлять транспортным средством в ЗТК в состоянии алкогольного, наркотического либо иного токсического опьянения и (или) передавать управление транспортного средства лицу, находящемуся в аналогичном состоянии;",
            "самостоятельно, без предварительного уведомления специалиста СВХ и разрешения таможенного органа покидать территорию ЗТК и (или) выезжать на транспортном средстве."
        ],
        "logo_path": logo_url
    }

    # Генерация HTML из шаблона
    html_string = render_to_string('pass_template.html', context)

    # Создание PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"{logbook.vehicle_number}_{logbook.id:07d}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    HTML(string=html_string).write_pdf(response)
    return response


#Обычные пользователи могут только читать данные пользователей.
#Только администраторы могут создавать, обновлять или удалять пользователей.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]  # Применение кастомного разрешения


# Склад временного хранения
class TSWViewSet(viewsets.ModelViewSet):
    queryset = TSW.objects.all()
    serializer_class = TSWSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


# Склад
class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


# Товар
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


# Рампа
class RampViewSet(ModelViewSet):
    queryset = Ramp.objects.all()
    serializer_class = RampSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


    #http://127.0.0.1:8000/api/v1/ramps/2/occupy/ - занята рампа, /free/ - свободна
    @action(detail=True, methods=['post'], url_path='occupy')
    def occupy_ramp(self, request, pk=None):
        """
        Машина занимает рампу (статус становится 'занято').
        """
        ramp = self.get_object()
        if ramp.status_ramp == "occupied":
            return Response({"error": "Рампа уже занята."}, status=status.HTTP_400_BAD_REQUEST)

        ramp.status_ramp = "occupied"
        ramp.save()
        return Response({"message": f"Рампа {ramp.description} занята."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='free')
    def free_ramp(self, request, pk=None):
        """
        Машина освобождает рампу (статус становится 'свободно').
        """
        ramp = self.get_object()
        if ramp.status_ramp == "free":
            return Response({"message": "Рампа уже свободна."}, status=status.HTTP_200_OK)

        ramp.status_ramp = "free"
        ramp.save()
        return Response({"message": f"Рампа {ramp.description} освобождена."}, status=status.HTTP_200_OK)


# Место складирования
class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

# Тип места
class TypePlaceViewSet(ModelViewSet):
    queryset = TypePlace.objects.all()
    serializer_class = TypePlaceSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

# Заказ услуги
class ServiceOrderViewSet(ModelViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

# Передача груза
class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

# Заказ
class OrderViewSet(MultiFieldFilterMixin, ModelViewSet):
    queryset = Order.objects.all().order_by('-id')  # Сортировка по id (самые ранние записи)
    serializer_class = OrderSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

    # Указываем поля для фильтрации сделанный через миксин
    filter_fields = ['carrier_name', 'vehicle_number']  # Поля для частичного поиска
    exact_filter_fields = ['warehouse_id']  # Поля для точного поиска

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        # Заполняем поле user текущим пользователем, если оно не передано
        serializer.save(user=self.request.user)


    # Использование миксина для поиска по полям
    # /orders/filter_orders/?warehouse=1
    @action(detail=False, methods=['get'])
    def filter_orders(self, request):
        return self.filter_by_fields(request)



    # запрос на поиск заказов по id и номеру авто
    # http://127.0.0.1:8000/api/v1/orders/search/?query=1

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Поиск заказов по частичному совпадению с ID, vehicle_number и фильтрацией по warehouse_id.
        Если параметры пустые, возвращает все записи.
        Если записи не найдены, возвращает пустой массив.
        """
        query = request.query_params.get('query', '').strip()
        warehouse_id = request.query_params.get('warehouse_id', '').strip()

        # Начинаем с полного queryset
        orders = self.queryset

        # Фильтрация по частичному совпадению ID или vehicle_number
        if query:
            orders = orders.filter(
                Q(id__icontains=query) | Q(vehicle_number__icontains=query)
            )

        # Фильтрация по warehouse_id
        if warehouse_id:
            orders = orders.filter(warehouse_id=warehouse_id)

        # Сортировка по id
        orders = orders.order_by('-id')

        # Пагинация
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если записи отсутствуют, возвращаем пустой массив
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Парковка
class ParkingViewSet(ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

# Парковочное место
class PlaceParkViewSet(ModelViewSet):
    queryset = PlacePark.objects.all()
    serializer_class = PlaceParkSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


    # Запрос на свободные парковочные места
    # /api/v1/place-parks/available/
    @action(detail=False, methods=['get'], url_path='available', url_name='available')
    def get_available_places(self, request):
        """
        Возвращает список доступных парковочных мест
        """
        available_places = PlacePark.objects.filter(is_available=True)
        serializer = self.get_serializer(available_places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Поставщик
class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


# Журнал учета
class LogBookViewSet(MultiFieldFilterMixin, ModelViewSet):
    queryset = LogBook.objects.select_related('warehouse', 'place_park', 'user_in', 'user_out').all().order_by('-id')
    serializer_class = LogBookSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

    # Указываем поля для фильтрации сделанный через миксин
    filter_fields = ['carrier_name', 'vehicle_number']  # Поля для частичного поиска
    exact_filter_fields = ['warehouse_id']  # Поля для точного поиска

    def get_serializer_class(self):
        if self.action == 'create':
            return LogBookCreateSerializer
        elif self.action == 'update_datetime_out':
            return LogBookUpdateSerializer
        return LogBookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Получение парковочного места
            place_park = serializer.validated_data.get('place_park')
            if place_park:
                if not place_park.is_available:
                    return Response({"error": "Парковочное место уже занято"}, status=status.HTTP_400_BAD_REQUEST)
                # Помечаем место как занятое
                place_park.is_available = False
                place_park.save()

            # Сохраняем запись и логируем
            serializer.save(user_in=request.user)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = self.get_object()

        # Обновление состояния парковочного места, если нужно
        new_place_park = serializer.validated_data.get('place_park')
        if new_place_park and new_place_park != instance.place_park:
            if not new_place_park.is_available:
                raise ValidationError("Новое парковочное место уже занято")
            if instance.place_park:
                instance.place_park.is_available = True
                instance.place_park.save()
            new_place_park.is_available = False
            new_place_park.save()

        # Сохраняем и логируем
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        # Если требуется освободить парковочное место
        if instance.place_park:
            instance.place_park.is_available = True
            instance.place_park.save()

        # Удаляем объект и логируем
        super().perform_destroy(instance)



    # Запрос через миксин на поиск по полям
    # api/v1/log-books/filter_orders/?warehouse_id=2&vehicle_number=
    @action(detail=False, methods=['get'])
    def filter_orders(self, request):
        """
        Фильтрация записей LogBook по указанным параметрам.
        """
        # Проверяем, переданы ли параметры фильтрации
        if not request.query_params:
            return Response([], status=200)  # Пустой массив

        # Проверяем, что значения всех параметров не пустые
        for key, value in request.query_params.items():
            if value == "":
                return Response([], status=200)  # Пустой массив

        # Используем миксин для получения отфильтрованного queryset
        queryset = self.filter_by_fields(request)

        if not queryset.exists():
            return Response([], status=200)  # Пустой массив

        # Пагинация и сериализация результата
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # PATCH / api / v1 / log - books / 1 / update - out /
    # {
    #     "datetime_out": "2024-12-03T18:00:00",
    #     "removed_control": "yes",
    #     "note": "Машина выехала"
    # }

    @action(detail=True, methods=['patch'], url_path='update-out')
    def update_datetime_out(self, request, pk=None):
        """
        Обновляет `datetime_out`, устанавливает `user_out` и освобождает место.
        """
        try:
            log_entry = self.get_object()
        except LogBook.DoesNotExist:
            return Response({"error": "Запись не найдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(log_entry, data=request.data, partial=True)
        if serializer.is_valid():
            # Освобождаем место, если связано с записью
            if log_entry.place_park:
                log_entry.place_park.is_available = True
                log_entry.place_park.save()

            # Устанавливаем `user_out` как текущего пользователя
            serializer.save(user_out=request.user)

            return Response(LogBookSerializer(log_entry).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # запрос на поиск заказов по id и номеру авто
    # http://127.0.0.1:8000/api/v1/log-books/search/?query=1
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Поиск заказов по частичному совпадению с ID, vehicle_number и фильтрацией по warehouse_id.
        Если параметры пустые, возвращает все записи.
        Если записи не найдены, возвращает пустой массив.
        """
        query = request.query_params.get('query', '').strip()
        warehouse_id = request.query_params.get('warehouse_id', '').strip()

        # Начинаем с полного queryset
        logbooks = self.queryset

        # Фильтрация по частичному совпадению ID или vehicle_number
        if query:
            logbooks = logbooks.filter(
                Q(id__icontains=query) | Q(vehicle_number__icontains=query)
            )

        # Фильтрация по warehouse_id
        if warehouse_id:
            logbooks = logbooks.filter(warehouse_id=warehouse_id)

        # Сортировка по id
        logbooks = logbooks.order_by('-id')

        # Пагинация
        page = self.paginate_queryset(logbooks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Если записи отсутствуют, возвращаем пустой массив
        serializer = self.get_serializer(logbooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Уведомление
class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Передаем текущего пользователя в сериализатор
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """
        Возвращаем другой сериализатор для PATCH запросов с исключением поля Order
        """
        if self.action == 'partial_update':  # PATCH запрос
            return NoticePatchSerializer
        return NoticeSerializer


    # Запрос на создание черновика с постоянными данными в таблице уведомление
    #/ api / v1 / notices / create - empty /
    # POST http://127.0.0.1:8000/api/v1/notices/create-empty/
    # {
    #   "order": 1
    # }
    # @action(detail=False, methods=['post'], url_path='create-empty')
    # def create_empty_notice(self, request):
    #     """
    #     Создает черновик уведомления с фиксированными данными и временем из LogBook.
    #     """
    #     user = request.user
    #     order_id = request.data.get('order')
    #
    #     if not order_id:
    #         return Response({'error': 'Необходимо указать заказ.'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         order = Order.objects.select_related('warehouse').get(id=order_id)
    #     except Order.DoesNotExist:
    #         return Response({'error': 'Заказ не найден.'}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # Получаем данные из Order
    #     vehicle_number = order.vehicle_number  # Номер машины из Order
    #
    #     # Получаем данные из Transport по номеру машины
    #     transport = Transport.objects.filter(ts=vehicle_number).first()
    #     transport_type = transport.type_ts if transport else None
    #     transport_country = transport.country if transport else None
    #
    #     # Генерация GUID
    #     guid = str(uuid.uuid4()).upper()
    #
    #     # Получаем номер склада из связанной таблицы Warehouse
    #     svh_number = order.warehouse.svh_number if order.warehouse else None
    #
    #     # Создаем уведомление
    #     notice = Notice.objects.create(
    #         user=user,
    #         order=order,
    #         stz="0",
    #         zhurnal="9",
    #         year=str(datetime.now().year)[-1],
    #         guid=guid,
    #         date_in=order.logbook.datetime_in.date() if order.logbook else None,  # Устанавливаем дату из LogBook
    #         time_in=order.logbook.datetime_in.time() if order.logbook else None,  # Устанавливаем время из LogBook
    #     )
    #
    #     # Устанавливаем дополнительные значения
    #     notice.number_out = str(notice.id)
    #     notice.notification = f"{'0' * (5 - len(str(notice.id)))}{notice.id}"
    #     notice.number_notification = f"ВЗ16466/0000304/{notice.year}{notice.zhurnal}{notice.stz}{str(notice.id).zfill(5)}"
    #     notice.save()
    #
    #     # Возвращаем заполненное уведомление
    #     serializer = self.get_serializer(notice)
    #     response_data = serializer.data
    #     response_data['svh_number'] = svh_number  # Добавляем номер склада в ответ
    #
    #     return Response(response_data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['post'], url_path='create-empty')
    def create_empty_notice(self, request):
        """
        Создает черновик уведомления с фиксированными данными, включая данные из Transport.
        """
        user = request.user
        order_id = request.data.get('order')

        if not order_id:
            return Response({'error': 'Необходимо указать заказ.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.select_related('warehouse').get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден.'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем данные из Order
        vehicle_number = order.vehicle_number  # Номер машины из Order

        # Получаем данные из Transport по номеру машины
        transport = Transport.objects.filter(ts=vehicle_number).first()
        transport_data = {
            "ts": transport.ts if transport else None,
            "type_ts": transport.type_ts if transport else None,
            "country": transport.country if transport else None
        }

        # Генерация GUID
        guid = str(uuid.uuid4()).upper()

        # Получаем номер склада из связанной таблицы Warehouse
        svh_number = order.warehouse.svh_number if order.warehouse else None

        # Создаем уведомление
        notice = Notice.objects.create(
            user=user,
            order=order,
            stz="0",
            zhurnal="9",
            year=str(datetime.now().year)[-1],
            guid=guid,
            date_in=order.logbook.datetime_in.date() if order.logbook else None,  # Устанавливаем дату из LogBook
            time_in=order.logbook.datetime_in.time() if order.logbook else None,  # Устанавливаем время из LogBook
        )

        # Устанавливаем дополнительные значения
        notice.number_out = str(notice.id)
        notice.notification = f"{'0' * (5 - len(str(notice.id)))}{notice.id}"
        notice.number_notification = f"ВЗ16466/0000304/{notice.year}{notice.zhurnal}{notice.stz}{str(notice.id).zfill(5)}"
        notice.save()

        # Возвращаем заполненное уведомление
        serializer = self.get_serializer(notice)
        response_data = serializer.data
        response_data.update(transport_data)  # Добавляем данные о транспорте в ответ
        response_data['svh_number'] = svh_number  # Добавляем номер склада в ответ

        return Response(response_data, status=status.HTTP_201_CREATED)




    # Поиск уведолмения по id заказа
    # /api/v1/notices/by-order/1/
    @action(detail=False, methods=['get'], url_path='by-order/(?P<order_id>[^/.]+)', url_name='by-order')
    def get_notices_by_order_id(self, request, order_id=None):
        """
        Получает уведомления по ID заказа вместе с документами, получателями и транспортом.
        """
        try:
            # Получаем уведомления по ID заказа
            notices = Notice.objects.filter(order_id=order_id).prefetch_related('docs', 'recipient')
            if not notices.exists():
                return Response(
                    {"error": f"Уведомления для заказа с ID {order_id} не найдены."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = NoticeSerializer(notices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






# Документ
class DocViewSet(ModelViewSet):
    queryset = Doc.objects.all()
    serializer_class = DocSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Обрабатываем POST-запрос для создания документа.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохраняем документ и возвращаем notice_id
        doc = serializer.save()
        response_data = serializer.data
        response_data['notice_id'] = doc.notice.id  # Добавляем поле notice_id
        return Response(response_data, status=status.HTTP_201_CREATED)


# Информация о перемещении товара по местам
class LogPlaceViewSet(ModelViewSet):
    queryset = LogPlace.objects.select_related('product', 'place_from', 'place_to', 'user').all()
    serializer_class = LogPlaceSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]



# Получатель
class RecipientViewSet(ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]


# Транспорт
class TransportViewSet(AuditLogMixin, ModelViewSet):
    queryset = Transport.objects.all().order_by('-id')
    serializer_class = TransportSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]

    # Поиск по t/s
    # http://127.0.0.1:8000/transports/search_by_ts/?q=4
    @action(detail=False, methods=['get'])
    def search_by_ts(self, request):
        search_query = request.query_params.get('q', '').strip()
        if not search_query:
            return Response({"error": "Неверный параметр ввода"}, status=400)

        # Выполняем фильтрацию
        transports = self.queryset.filter(Q(ts__iregex=search_query)).order_by('-id')[:6]

        # Проверяем результат
        if not transports.exists():
            return Response({"message": "false"}, status=404)

        # Сериализуем результат
        serializer = self.get_serializer(transports, many=True)
        return Response(serializer.data)

    # Поиск по t/s и по carrier_name
    # http://127.0.0.1:8000/transports/search_by_ts_and_carrier_name/?q=4
    @action(detail=False, methods=['get'])
    def search_by_ts_and_carrier_name(self, request):
        search_query = request.query_params.get('q', '').strip()

        # Если параметр q пуст, возвращаем все записи
        if not search_query:
            transports = self.queryset
        else:
            # Фильтрация по ts и carrier_name
            transports = self.queryset.filter(
                Q(ts__iregex=search_query) | Q(carrier_name__iregex=search_query)
            )

        # Проверяем результат
        if not transports.exists():
            return Response({"message": "false"}, status=404)

        # Применяем пагинацию через AllOtherAPIListPagination
        page = self.paginate_queryset(transports)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Сериализуем результат без пагинации
        serializer = self.get_serializer(transports, many=True)
        return Response(serializer.data)







# Транспорт-Уведомление
class TransportNoticeViewSet(ModelViewSet):
    queryset = TransportNotice.objects.all()
    serializer_class = TransportNoticeSerializer
    pagination_class = AllOtherAPIListPagination
    permission_classes = [IsAuthenticated]




# Запрос на справочники
# http://127.0.0.1:8000/api/v1/directories/countries/
# Справочники находятся в directory.py
class DirectoryView(APIView):
    """
    API для предоставления справочников в формате массива объектов.
    """
    def get(self, request, *args, **kwargs):
        directory_name = kwargs.get('directory_name')
        directories = {
            'http_answer': HTTP_ANSWER,
            'languages': LANG,
            'status_reg': STATUS_REG,
            'ln_type': LN_TYPE,
            'countries': COUNTRY,
            'currencies': CURRENCY_CHOICES,
            'purpose_types': PURPOSE_TYPES,
            'type_service': TYPE_SERVICE,
            'type_ts': TYPE_TS,
            'type_ts_choises': TRANSPORT_TYPE_CHOICES,


        }

        if directory_name in directories:
            data = directories[directory_name]

            # Преобразуем список пар в массив объектов
            result = [{"код": item[0], "название": item[1]} for item in data]

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": f"Справочник '{directory_name}' не найден."},
                status=status.HTTP_404_NOT_FOUND
            )


class AuditLogMixin:
    """
    Миксин для автоматического логирования действий пользователя.
    """

    def log_action(self, user, obj=None, description=None):
        """
        Логирует действие пользователя.
        """
        content_type = ContentType.objects.get_for_model(obj) if obj else None
        object_id = obj.id if obj else None
        UserActionLog.objects.create(
            user=user,
            content_type=content_type,
            object_id=object_id,
            description=description
        )

    def log_action_from_request(self, obj=None, description=None):
        """
        Упрощенный метод для логирования действия с текущим пользователем из запроса.
        """
        self.log_action(self.request.user, obj, description)

    def perform_update(self, serializer):
        """
        Логирование обновления объекта с фиксацией изменений.
        """
        obj = self.get_object()
        updated_obj = serializer.save()
        self.log_action_from_request(
            updated_obj,
            f"Обновлен объект {updated_obj}"
        )
        return updated_obj

    def perform_create(self, serializer):
        """
        Логирование создания объекта.
        """
        obj = serializer.save()
        self.log_action_from_request(
            obj,
            f"Создан объект {obj}"
        )
        return obj

    def perform_destroy(self, instance):
        """
        Логирование удаления объекта.
        """
        self.log_action_from_request(
            instance,
            f"Удален объект {instance}"
        )
        super().perform_destroy(instance)


class UserActionLogViewSet(ReadOnlyModelViewSet):
    queryset = UserActionLog.objects.all().order_by('-datetime')
    serializer_class = UserActionLogSerializer
    permission_classes = [IsAdminUser]

