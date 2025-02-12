from rest_framework import serializers
from .models import *
from django.utils.timezone import localtime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        #  Добавляем данные пользователя в токен
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name

        return data


# Пользователь
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']


# Склад временного хранения
class TSWSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSW
        fields = '__all__'


# Склад
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['name']


# Товар
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Рампа
class RampSerializer(serializers.ModelSerializer):
    status_ramp_display = serializers.CharField(source='get_status_ramp_display', read_only=True)

    class Meta:
        model = Ramp
        fields = ['id', 'description', 'note', 'status_ramp', 'status_ramp_display']

    #Меняем статус рампы автоматически через пост запрос
    def validate_status_ramp(self, value):
        # Преобразуем отображаемые значения в технические
        display_to_value = {
            "Занято": "occupied",
            "Свободно": "free"
        }
        if value in display_to_value:
            return display_to_value[value]
        elif value in ["occupied", "free"]:
            return value
        raise serializers.ValidationError("Некорректный статус рампы. Используйте 'Занято' или 'Свободно'.")




# Место складирования
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


# Тип места
class TypePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePlace
        fields = '__all__'


# Заказ услуги
class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'


# Передача груза
class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'


# Заказ
class LogBookDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о LogBook"""
    class Meta:
        model = LogBook
        fields = '__all__'  # Поля, которые мы хотим отобразить для GET-запроса


# Прикрепленные файлы для таблицы Document
class DocumentFileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = DocumentFile
        fields = ['id', 'order', 'file', 'file_name', 'uploaded_at', 'description']

    def get_file_name(self, obj):
        return obj.get_file_name()




class OrderSerializer(serializers.ModelSerializer):
    """Основной сериализатор для Order"""
    logbook = serializers.SerializerMethodField()
    seal = serializers.SerializerMethodField()
    seal_quantity = serializers.SerializerMethodField()
    seal_number = serializers.SerializerMethodField()
    notice_id = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    files = DocumentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # Все поля модели Order + дополнительные

    def get_logbook(self, obj):
        # Для GET-запросов возвращаем подробный сериализатор LogBook
        request = self.context.get('request')
        if request and request.method == 'GET' and obj.logbook:
            return LogBookDetailSerializer(obj.logbook).data
        # Для POST-запросов возвращаем только ID
        return obj.logbook.id if obj.logbook else None

    def get_seal(self, obj):
        # Возвращаем значение seal из логбука, если он существует
        return obj.logbook.seal if obj.logbook else None

    def get_seal_quantity(self, obj):
        # Возвращаем значение seal_quantity из логбука, если он существует
        return obj.logbook.seal_quantity if obj.logbook else None

    def get_seal_number(self, obj):
        # Возвращаем значение seal_number из логбука, если он существует
        return obj.logbook.seal_number if obj.logbook else None

    def get_vehicle_number(self, obj):
        # Возвращаем значение vehicle_number из логбука, если он существует
        return obj.logbook.vehicle_number if obj.logbook else None

    def get_notice_id(self, obj):
        # Если есть уведомление, возвращаем его ID, иначе возвращаем False
        notice = obj.notices.first()
        return notice.id if notice else False




class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания Order (только id для logbook)"""
    logbook = serializers.PrimaryKeyRelatedField(
        queryset=LogBook.objects.all(),  # Указываем queryset для выбора id
        required=True  # Поле обязательно при создании
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Поле user автоматически подставляется

    class Meta:
        model = Order
        fields = '__all__'


# Парковка
class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


# Парковочное место
class PlaceParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacePark
        fields = '__all__'


# Поставщик
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


# Журнал учета
class LogBookSerializer(serializers.ModelSerializer):
    warehouse = serializers.CharField(source='warehouse.name', read_only=True)
    place_park = serializers.SerializerMethodField()
    user_in = serializers.CharField(source='user_in.username', read_only=True)
    user_out = serializers.CharField(source='user_out.username', read_only=True)

    class Meta:
        model = LogBook
        fields = [
            'id',
            'warehouse',
            'status', 'carrier_info', 'vehicle_number', 'trailer_number', 'phone', 'seal', 'seal_quantity', 'seal_number',
            'place_park', 'place_park_id', 'datetime_in', 'datetime_out', 'user_in', 'user_out', 'note', 'note_in', 'note_out'
        ]
        read_only_fields = ['note_out']

    def get_place_park(self, obj):
        return f"{obj.place_park.spot_number}" if obj.place_park else None


class LogBookCreateSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), required=True, label="Склад"
    )
    place_park = serializers.PrimaryKeyRelatedField(
        queryset=PlacePark.objects.filter(is_available=True),
        required=False,
        label="Парковочное место (можно оставить пустым)",
    )

    class Meta:
        model = LogBook
        fields = [
            'warehouse',
            'place_park', 'status', 'carrier_info', 'vehicle_number', 'trailer_number', 'phone', 'seal', 'seal_quantity', 'seal_number',
            'datetime_in', 'note_in', 'note'
        ]

    def validate(self, data):
        if not data.get('place_park') and not PlacePark.objects.filter(
            parking__warehouse=data['warehouse'], is_available=True
        ).exists():
            raise serializers.ValidationError("Нет доступных парковочных мест для выбранного склада.")
        return data

    def create(self, validated_data):
        # Автоматическое назначение парковочного места
        place_park = validated_data.get('place_park')
        if not place_park:
            warehouse = validated_data['warehouse']
            place_park = PlacePark.objects.filter(parking__warehouse=warehouse, is_available=True).first()
            place_park.is_available = False
            place_park.save()

        validated_data['place_park'] = place_park
        return super().create(validated_data)


class LogBookUpdateSerializer(serializers.ModelSerializer):
    user_out = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LogBook
        fields = ['datetime_out', 'note_out', 'note', 'user_out']

    def validate(self, data):
        # Проверка, что время выезда позже времени въезда
        if 'datetime_out' in data and self.instance.datetime_in:
            if data['datetime_out'] <= self.instance.datetime_in:
                raise serializers.ValidationError("Время выезда должно быть позже времени въезда.")
        return data


# Документ
class DocSerializer(serializers.ModelSerializer):
    """Сериализатор для документов"""
    class Meta:
        model = Doc
        fields = ['id', 'doc_code', 'doc_number', 'doc_date', 'notice']

    def to_representation(self, instance):
        # Для GET-запросов исключаем поле 'notice'
        request = self.context.get('request')
        representation = super().to_representation(instance)
        if request and request.method == 'GET':
            representation.pop('notice', None)  # Убираем поле 'notice' из ответа
        return representation



# Получатель
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id', 'name', 'country', 'notice']

    def to_representation(self, instance):
        # Для GET-запросов исключаем поле 'notice'
        request = self.context.get('request')
        representation = super().to_representation(instance)
        if request and request.method == 'GET':
            representation.pop('notice', None)  # Убираем поле 'notice' из ответа
        return representation
    




# Транспорт-Уведомление
class TransportNoticeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TransportNotice
        fields = ['id', 'notice', 'number', 'type', 'country']

    def create(self, validated_data):
        # Проверяем или создаем транспортное средство
        ts_number = validated_data.get('number')
        transport, created = Transport.objects.get_or_create(
            ts=ts_number,
            defaults={
                "type_ts": validated_data.get("type", ""),
                "country": validated_data.get("country", "")
            }
        )

        if not created:
            # Если транспортное средство существует, обновляем его данные
            transport.type_ts = validated_data.get("type", transport.type_ts)
            transport.country = validated_data.get("country", transport.country)
            transport.save()

        # Создаем запись в таблице TransportNotice
        transport_notice = super().create(validated_data)

        return transport_notice


# Уведомление
class NoticeSerializer(serializers.ModelSerializer):
    id_notice = serializers.SerializerMethodField()
    docs = DocSerializer(many=True, read_only=True)
    recipient = RecipientSerializer(many=True, read_only=True)
    transport = serializers.SerializerMethodField()
    svh_number = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  # Добавляем поле status

    class Meta:
        model = Notice
        fields = [
            'id_notice', 'date_in', 'guid', 'time_in', 'order', 'gross_weight',
            'goods_presence', 'purpose_placement', 'direction_vehicle', 'number_out',
            'notification', 'number_notification', 'zhurnal',
            'stz', 'year', 'fio', 'docs', 'recipient', 'transport',
            'svh_number', 'status'  # Добавляем status
        ]
        read_only_fields = [
            'id_notice', 'number_out', 'notification', 'number_notification',
            'zhurnal', 'stz', 'year', 'guid', 'doc_creation_date', 'fio'
        ]

    def get_id_notice(self, obj):
        return obj.id

    def get_transport(self, obj):
        transport_notices = TransportNotice.objects.filter(notice=obj)
        return [
            {
                "id": tn.id,
                "ts": tn.number,
                "type_ts": tn.type,
                "country": tn.country
            }
            for tn in transport_notices
        ]

    def get_svh_number(self, obj):
        if obj.order and obj.order.warehouse:
            return obj.order.warehouse.svh_number or "СВ-1601/0000304"
        return "СВ-1601/0000304"

    def get_status(self, obj):
        """Получаем статус из EClient по GUID"""
        eclient_entry = EClient.objects.using('second_db').filter(guidXML=obj.guid).first()
        return eclient_entry.status if eclient_entry else "Не найден"


class NoticePatchSerializer(serializers.ModelSerializer):
    id_notice = serializers.SerializerMethodField()
    docs = DocSerializer(many=True, read_only=True)
    recipient = RecipientSerializer(many=True, read_only=True)
    transport = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id_notice', 'date_in', 'time_in', 'gross_weight',
            'goods_presence', 'purpose_placement', 'number_out',
            'notification', 'number_notification', 'zhurnal',
            'stz', 'year', 'fio', 'docs', 'recipient', 'transport'
        ]  # Поле 'order' удалено
        read_only_fields = [
            'id_notice', 'number_out', 'notification', 'number_notification',
            'zhurnal', 'stz', 'year', 'guid', 'doc_creation_date', 'fio'
        ]

    def get_id_notice(self, obj):
        return obj.id

    def get_transport(self, obj):
        transport_notices = TransportNotice.objects.filter(notice=obj)
        return [
            {
                "id": tn.id,
                "ts": tn.number,
                "type_ts": tn.type,
                "country": tn.country
            }
            for tn in transport_notices
        ]



# Перемещение товара по местам на складе
class LogPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogPlace
        fields = '__all__'


# Транспорт
class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'


# Таблица регистрации с другой БД
class EClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EClient
        fields = '__all__'


class UserActionLogSerializer(serializers.ModelSerializer):
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    formatted_datetime = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = UserActionLog
        fields = [
            'id',
            'user',
            'user_first_name',
            'user_last_name',
            'content_type',
            'content_type_name',
            'object_id',
            'action',
            'action_display',
            'action_user',
            'description',
            'formatted_datetime'
        ]

    def get_formatted_datetime(self, obj):
        # Преобразуем время в локальный часовой пояс (Минск)
        return localtime(obj.datetime).strftime("%Y-%m-%d %H:%M:%S")