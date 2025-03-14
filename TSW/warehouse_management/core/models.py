from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .directory import *
import re
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now, localtime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
import json
import uuid
from django.conf import settings
import os
from django.utils import timezone
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
import random



# Склад временного хранения, от него идет дальше в перспективе что складов будет много
class TSW(models.Model):
    name = models.CharField("Название склада", max_length=100)
    base_notification_number = models.CharField(
        "Базовый номер уведомлений (например, ВЗ/номер_СВХ)",
        max_length=50,
        unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Склад временного хранения"
        verbose_name_plural = "Склады временного хранения"

    def __str__(self):
        return f"Склад {self.name} ({self.base_notification_number})"


#Склад
class Warehouse(models.Model):
    TSW = models.ForeignKey('TSW', on_delete=models.PROTECT, verbose_name='Склад временного хранения')
    name = models.CharField("Название склада", max_length=100)
    svh_number = models.CharField("Номер СВХ", max_length=50, blank=True, null=True, help_text="Номер СВХ для склада")
    address = models.CharField("Адрес склада", max_length=100)
    note = models.TextField("Примечание", blank=True, null=True)
    place = models.ForeignKey('Place', on_delete=models.PROTECT, related_name='warehouses',
                              verbose_name="Места складирования", blank=True, null=True)
    customs_post = models.CharField("Номер поста таможни", max_length=100, blank=True, null=True)
    name_post = models.CharField("Название поста", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"{self.name} (СВХ: {self.svh_number})"

    def save(self, *args, **kwargs):
        # Устанавливаем номер поста таможни по умолчанию
        if not self.customs_post:
            self.customs_post = "16466"

        # Устанавливаем название поста по умолчанию
        if not self.name_post:
            self.name_post = "Бенякони ТЛЦ"

        # Устанавливаем постоянный номер СВХ
        if not self.svh_number:
            self.svh_number = "СВ-1601/0000304"  # Устанавливаем номер СВХ

        super().save(*args, **kwargs)


#Рампа куда заезжает водитель на выгрузку / загрузку
class Ramp(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='ramps', verbose_name="Склад")
    description = models.CharField("Описание рампы", max_length=100)
    note = models.TextField("Примечание", blank=True, null=True)
    status_ramp = models.CharField(
        "Статус занято / не занято", max_length=20, choices=STATUS_RAMP_CHOICES)


    class Meta:
        verbose_name = "Рампа"
        verbose_name_plural = "Рампы"

    def __str__(self):
        return f"{self.description} - {self.get_status_ramp_display()}"


# Закзачик ( клиент ) - есть поле charfield в таблице ORDER
# class Customer(models.Model):
#     name = models.CharField("Название перевозчика", max_length=255)
#     contact_info = models.CharField("Контактная информация", max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.name


# Товар
class Product(models.Model):
    pallet = models.ForeignKey('Pallet', on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    sku_product = models.CharField("Штрихкод EAN-13", max_length=13, unique=True, blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    code_product = models.CharField("Код товара с документа (CMR/INVOICE)", max_length=100)
    type_product = models.CharField("Тип товара", max_length=100)
    description = models.TextField("Описание товара", blank=True, null=True)
    net_weight = models.DecimalField("Вес нетто", max_digits=10, decimal_places=2)
    gross_weight = models.DecimalField("Вес брутто", max_digits=10, decimal_places=2)
    quantity = models.IntegerField("Количество")
    quantity_dispatched = models.IntegerField("Отгружено", default=0)
    # customer = models.ForeignKey('customer', on_delete=models.SET_NULL, related_name='products', null=True,  blank=True)  # Заказчик ( таблица отдельная)
    # carrier = models.ForeignKey('Carrier', on_delete=models.SET_NULL, related_name='products', null=True, blank=True)  # Перевозчик ??? есть в журнале
    doc = models.ForeignKey('Doc', on_delete=models.SET_NULL, related_name='products', null=True, blank=True, verbose_name="DOC")
    # recipient = models.ForeignKey('Recipient', on_delete=models.SET_NULL, related_name='products', null=True, blank=True)   # Связь с получателем ??? есть таблица
    notice = models.ForeignKey('Notice', on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    status = models.CharField("Статус", max_length=50, choices=STATUS_PRODUCT, default='Ожидает приемки')
    datetime_in = models.DateTimeField("Время прибытия товара", blank=True, null=True)
    datetime_out = models.DateTimeField("Время убытия товара", blank=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.sku_product} - {self.type_product}"


    # Создание штрихкода. В админке вводится в ручную, в API автоматиечески. Генерация исключительно цифры
    def generate_ean13(self):
        base_code = f"{self.code_product}{int(time.time())}"[-13:]  # Уникальный код
        ean = barcode.get('ean13', base_code, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode_image.save(f'barcode_ean13_{base_code}.png', File(buffer), save=False)
        self.sku_product = base_code
        buffer.close()

    def save(self, *args, **kwargs):
        if not self.pallet:  # Если товара нет на паллете – генерируем штрихкод
            if not self.sku_product:
                self.generate_ean13()
        else:
            self.sku_product = None  # Если товар на паллете, штрихкод не нужен

        super().save(*args, **kwargs)



# Таблица паллетов если мы используем штрихкод для паллетированного груза
class Pallet(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='pallets')
    sku_pallet = models.CharField("Штрихкод ITF-14", max_length=14, unique=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    description = models.CharField("Описание", max_length=255, blank=True, null=True)
    datetime_in = models.DateTimeField("Время прибытия")
    datetime_out = models.DateTimeField("Время убытия", blank=True, null=True)
    current_weight = models.DecimalField("Текущий вес (кг)", max_digits=10, decimal_places=2, default=0)
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Паллет"
        verbose_name_plural = "Паллеты"

    def __str__(self):
        return self.sku_pallet

    # Создание штрихкода. В админке вводится в ручную, в API автоматиечески. Генерация исключительно цифры

    def generate_itf14(self):
        base_code = ''.join([str(random.randint(0, 9)) for _ in range(14)])  # Генерация 14-значного кода
        itf = barcode.get('itf', base_code, writer=ImageWriter())
        buffer = BytesIO()
        itf.write(buffer)
        self.barcode_image.save(f'barcode_itf14_{base_code}.png', ContentFile(buffer.getvalue()), save=False)
        return base_code

    def save(self, *args, **kwargs):
        if not self.sku_pallet:  # Проверяем, есть ли код, если нет - генерируем
            self.sku_pallet = self.generate_itf14()  # Генерируем и сохраняем код
        super().save(*args, **kwargs)

# Перемещение товара по местам
class LogPlace(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='log_places', verbose_name='Товар', null=True, blank=True)
    pallet = models.ForeignKey('Pallet', on_delete=models.CASCADE, related_name='log_places', verbose_name='Паллет', null=True, blank=True)
    place_from = models.ForeignKey('Place', on_delete=models.SET_NULL, null=True, blank=True, related_name='log_places_from', verbose_name="Место откуда")
    place_to = models.ForeignKey('Place', on_delete=models.CASCADE, related_name='log_places_to', verbose_name="Место куда")
    quantity = models.PositiveIntegerField("Количество перемещаемого товара/паллета")
    weight = models.DecimalField("Вес (кг)", max_digits=10, decimal_places=2, blank=True, null=True)
    datetime = models.DateTimeField("Дата и время перемещения", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_places', verbose_name="Пользователь")
    barcode_type = models.CharField("Тип штрихкода", max_length=10, choices=[('EAN-13', 'EAN-13'), ('ITF-14', 'ITF-14')], default='EAN-13')
    status = models.CharField("Статус", max_length=50, choices=STATUS_PRODUCT, default='Перемещено')
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Лог перемещения товара"
        verbose_name_plural = "Логи перемещений товара"

    def __str__(self):
        return f"Перемещение {self.product.sku} ({self.quantity} ед.) с {self.place_from} на {self.place_to}"






#Место складирования
class Place(models.Model):
    type_place = models.ForeignKey('TypePlace', on_delete=models.CASCADE)
    status_place = models.CharField("Статус ", max_length=50, choices=STATUS_CHOICES) # занято свободно частично занято
    type = models.CharField("Тип места", max_length=100)
    characteristic = models.CharField("Характеристика места", max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Место складирования"
        verbose_name_plural = "Места складирования"

    def __str__(self):
        return f"{self.description} - {self.get_status_place_display()}"




#Описание места
class TypePlace(models.Model):
    description = models.TextField("Описание")
    max_weight = models.DecimalField("Максимальный вес (кг)", max_digits=10, decimal_places=2)
    max_size = models.CharField("Максимальный размер (кг)", max_length=100)
    type_product = models.CharField("Тип товара", max_length=100)
    type_place = models.CharField("Тип места (европаллет и тд)", max_length=100)
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Тип места"
        verbose_name_plural = "Типы мест"

    def __str__(self):
        return self.type_place



# Заказ услуги
class ServiceOrder(models.Model):
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    price_nds = models.DecimalField("Цена с НДС", max_digits=10, decimal_places=2)
    price_invoice = models.DecimalField("Цена по инвойсу", max_digits=10, decimal_places=2)
    description_service = models.TextField("Описание услуги")
    note = models.TextField("Примечание", blank=True, null=True)
    currency = models.CharField("Валюта", max_length=3, choices=CURRENCY_CHOICES)

    class Meta:
        verbose_name = "Заказ услуги"
        verbose_name_plural = "Заказы услуг"

    def __str__(self):
        return self.description_service



# Передача груза
class Transfer(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='transfers', verbose_name='Товар')  # нельзя удалять
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transfers', verbose_name='Пользователь')  # нельзя удалять
    order_in = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='transfers_in')  # нельзя удалять
    order_out = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='transfers_out')  # нельзя удалять
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество")
    note = models.TextField("Примечание", blank=True, null=True)
    type_transfer = models.CharField("Тип трансфера", max_length=100)
    is_fully_transferred = models.BooleanField("Товар забран полностью", default=False)

    class Meta:
        verbose_name = "Передача груза"
        verbose_name_plural = "Передачи грузов"

    def save(self, *args, **kwargs):
        """
        Автоматически обновляет статус 'is_fully_transferred' в зависимости от количества.
        """
        product_quantity = self.product.quantity  # в модели Product есть поле quantity
        if self.quantity >= product_quantity:
            self.is_fully_transferred = True
        else:
            self.is_fully_transferred = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Трансфер {self.id}: {self.type_transfer} ({'Полностью' if self.is_fully_transferred else 'Частично'})"



# Заказ
class Order(models.Model):
    logbook = models.ForeignKey('LogBook', on_delete=models.DO_NOTHING, related_name='orders', verbose_name='Журнал въезда/выезда', blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='orders', verbose_name='Склад')
    transport_type = models.CharField("Тип транспорта", max_length=1, choices=TRANSPORT_TYPE_CHOICES,
                                      default='A')
    carrier_name = models.CharField("ФИО водителя (перевозчик)", max_length=100)
    phone = models.CharField("Телефон водителя", max_length=20)
    vehicle_number = models.CharField("Номер т/с", max_length=20)
    supplier = models.ForeignKey('Supplier', on_delete=models.DO_NOTHING, verbose_name="Отправитель / Получатель (Поставщик)", blank=True, null=True)
    customer = models.CharField("Заказчик", max_length=100, blank=True, null=True)
    status_order = models.CharField("Статус заказа", max_length=2, default='0', choices=STATUS_ORDER)
    datetime = models.DateTimeField("Дата и время заказа")
    quantity = models.PositiveIntegerField("Количество партий")
    damage = models.BooleanField("Повреждение груза", default=False)
    damage_description = models.TextField("Описание повреждения", blank=True, null=True)
    user = models.ForeignKey(User, blank=False, on_delete=models.DO_NOTHING, verbose_name="Пользователь", related_name='orders')
    note = models.TextField("Примечание", blank=True, null=True)


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def clean(self):
        super().clean()
        if self.damage == 'true' and not self.damage_description:
            raise ValidationError("Пожалуйста, укажите описание повреждения, так как повреждение есть.")

    def __str__(self):
        return f"Заказ id {self.id} - Статус {self.status_order}"



# Парковка т/с на СВХ
class Parking(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='parkings', verbose_name='Склад')
    description = models.TextField("Описание", blank=True, null=True)
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Парковка"
        verbose_name_plural = "Парковки"

    def __str__(self):
        return self.description or "Парковка без описания"




# Парковочное место т/с
class PlacePark(models.Model):
    parking = models.ForeignKey('Parking', on_delete=models.CASCADE, related_name='places', verbose_name='Парковка')
    spot_number = models.CharField("Номер парковочного места", max_length=50)
    size = models.CharField("Размер", max_length=50, blank=True, null=True)
    is_available = models.BooleanField("Доступность", default=True)



    class Meta:
        verbose_name = "Парковочное место"
        verbose_name_plural = "Парковочные места"

    @staticmethod
    def get_nearest_available():
        """
        Находит ближайшее свободное парковочное место.
        """
        return PlacePark.objects.filter(is_available=True).order_by('spot_number').first()

    def __str__(self):
        return f"Парковка {self.parking.description} - Место {self.spot_number}"


# Поставщик ( заказчик / получатель )
class Supplier(models.Model):
    name = models.CharField("Название", max_length=100)
    address = models.TextField("Адрес", blank=True, null=True)
    postal_code = models.CharField("Индекс", max_length=20)
    phone = models.CharField("Телефон", max_length=20)
    city = models.CharField("Город", max_length=100)
    tax_number = models.CharField("Номер налогоплательщика", max_length=20)
    note = models.TextField("Примечание", blank=True, null=True)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name


# Журнал въезда выезда
class LogBook(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='log_entries', verbose_name='Склад', blank=True, null=True)
    status = models.CharField("Статус загрузки/выгрузки", max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    carrier_info = models.CharField("ФИО водителя", max_length=100)
    phone = models.CharField("телефон водителя", max_length=100)
    vehicle_number = models.CharField("Номер т/с", max_length=100)
    trailer_number = models.CharField("Номер прицепа", max_length=100, blank=True, null=True)
    seal = models.BooleanField("Пломба есть/нет", default=False) # сделано просто булевым
    seal_quantity = models.CharField("Количество пломб", max_length=100, blank=True, null=True)
    seal_number = models.CharField("Номер пломбы", max_length=100, blank=True, null=True)
    place_park = models.ForeignKey('PlacePark', on_delete=models.CASCADE, related_name='log_entries')
    removed_control = models.CharField("Снято с контроля", max_length=10, choices=REMOVED_CONTROL_CHOICES)
    datetime_in = models.DateTimeField("Дата и время прибытия")
    datetime_out = models.DateTimeField("Дата и время убытия", blank=True, null=True)
    user_in = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registered_by_log", verbose_name='Пользователь создал запись')
    user_out = models.ForeignKey(User, on_delete=models.CASCADE, related_name="removed_by_log", blank=True, null=True, verbose_name='Пользователь закрыл запись')
    note_in = models.TextField("Примечание при въезде", blank=True, null=True)
    note_out = models.TextField("Примечание при выезде", blank=True, null=True)
    note = models.TextField("Общее примечание", blank=True, null=True)



    class Meta:
        verbose_name = "Журнал въезда/выезда"
        verbose_name_plural = "Журналы въезда/выезда"

    def clean(self):
        super().clean()

        # Проверка на корректный формат vehicle_number
        if not re.fullmatch(r'^[A-Z0-9]+$', self.vehicle_number.replace("-", "").strip()):
            raise ValidationError({
                'vehicle_number': "Номер т/с должен содержать только латинские большие буквы и цифры без дефисов."
            })

        # Проверка даты выезда
        if self.datetime_out and self.datetime_in and self.datetime_out <= self.datetime_in:
            raise ValidationError("Дата убытия должна быть позже даты прибытия.")


        # Проверка пломбы
        # if self.seal == 'yes':
        #     if not self.seal_number:
        #         raise ValidationError("Пожалуйста, укажите номер пломбы, так как пломба есть.")
        #     if not self.seal_quantity:
        #         raise ValidationError("Пожалуйста, укажите количество пломб, так как пломба есть.")
        # else:
        #     # Если пломбы нет, количество и номер пломбы должны быть пустыми
        #     if self.seal_number or self.seal_quantity:
        #         raise ValidationError("Если пломбы нет, номер и количество пломб должны быть пустыми.")

        if self.seal:  # Если пломба есть (True) проверка пломбы так как вместо чоиза булен тип стоит
            if not self.seal_number:
                raise ValidationError({
                    'seal_number': "Пожалуйста, укажите номер пломбы, так как пломба есть."
                })
            if not self.seal_quantity:
                raise ValidationError({
                    'seal_quantity': "Пожалуйста, укажите количество пломб, так как пломба есть."
                })
        else:  # Если пломбы нет (False)
            if self.seal_number or self.seal_quantity:
                raise ValidationError({
                    'seal_number': "Если пломбы нет, номер пломбы должен быть пустым.",
                    'seal_quantity': "Если пломбы нет, количество пломб должно быть пустым."
                })

    def save(self, *args, **kwargs):
        # Преобразование vehicle_number перед сохранением
        if self.vehicle_number:
            self.vehicle_number = self.vehicle_number.replace("-", "").upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"LogBook {self.vehicle_number} ({self.datetime_in})"



# Таблица уведомлений
class Notice(models.Model):
    doc_creation_date = models.DateTimeField("Дата и время создания документа", auto_now_add=True)
    date_in = models.DateField("Дата въезда") # берем с журнала
    time_in = models.TimeField("Время въезда") # берем с журнала
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='notices', verbose_name='Заказ')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='notices', verbose_name='Пользователь')
    # gross_weight = models.FloatField("Вес брутто")
    gross_weight = models.DecimalField("Вес брутто", max_digits=10, decimal_places=2, null=True, blank=True)
    goods_presence = models.BooleanField("Наличие товара", default=False)
    purpose_placement = models.CharField("Цель размещения", max_length=2, choices=PURPOSE_TYPES, default='22')
    direction_vehicle = models.CharField("Направление т/с", max_length=1, choices=DIRECTION_TYPES, default='2')
    # автоматически формируемые поля
    guid = models.CharField(max_length=36, default=uuid.uuid4, unique=True, verbose_name="GUID номер")
    number_out = models.CharField(max_length=15, verbose_name="Исходящий номер", blank=True, null=True)  # id notice
    notification = models.CharField(max_length=25, verbose_name="Уведомление", blank=True, null=True) #00000 id notice
    number_notification = models.CharField(max_length=50, verbose_name="Номер уведомления", blank=True, null=True)  # с нескольких полей делаем
    zhurnal = models.CharField(max_length=12, verbose_name="Журнал", blank=True, null=True) # автоматически 9
    stz = models.CharField(max_length=1, verbose_name="СТЗ", blank=True, null=True)  # автоматически 0
    year = models.CharField(max_length=12, verbose_name="Год", blank=True, null=True)  # автоматически цифра года
    unp = models.CharField("УНП компании", max_length=15, editable=False, default="591489147")
    fio = models.CharField(
        max_length=100,
        default="Мартинкевич Сергей Анатольевич",
        verbose_name="ФИО ответственного лица",
        blank=True,
        null=True
    ) # пока оставляем текстовое поле

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Уведомление id {self.id} для заказа id {self.order.id}"




class Transport(models.Model):
    ts = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Номер транспортного средства")
    type_ts = models.CharField(max_length=3, blank=True, choices=TYPE_TS, verbose_name="Тип")
    country = models.CharField(max_length=2, blank=True, choices=COUNTRY, verbose_name="Страна транспортного средства")
    carrier_name = models.CharField(max_length=100, default='', verbose_name="Перевозчик")

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = "Транспорты"

    def __str__(self):
        return f'{self.ts}-{self.type_ts}-{self.country}'


class TransportNotice(models.Model):
    notice = models.ForeignKey('Notice', on_delete=models.CASCADE, related_name='transport_notice', verbose_name='Уведомление')
    number = models.CharField("Номер", max_length=100)
    type = models.CharField("Тип", max_length=100)
    country = models.CharField(max_length=2, blank=True, choices=COUNTRY, verbose_name="страна транспортного средства")


    class Meta:
        verbose_name = 'Транспорт-Уведомление'
        verbose_name_plural = "Транспорты-Уведомления"

    def __str__(self):
        return f'{self.notice}-{self.number}-{self.type}'


# Документы
class Doc(models.Model):
    notice = models.ForeignKey('Notice', on_delete=models.CASCADE, verbose_name="Уведомление", related_name='docs')
    doc_code = models.CharField(max_length=5, choices=TYPE_VID_DOC, verbose_name="Код документа")
    doc_number = models.CharField(max_length=30, default='-', verbose_name="Номер документа")
    doc_date = models.DateField(verbose_name="Дата документа")


    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"{self.doc_number} от {self.doc_date} ({self.doc_code})"


class DocumentFile(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Заказ", related_name='files')
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    description = models.TextField(blank=True, null=True, verbose_name="Описание файла")

    class Meta:
        verbose_name = "Файл документа"
        verbose_name_plural = "Файлы документов"


    # Сохранение файлов а папке media/documents/notice_id
    def save(self, *args, **kwargs):
        folder_path = os.path.join('documents', str(self.order.id))
        absolute_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
        os.makedirs(absolute_folder_path, exist_ok=True)
        self.file.field.upload_to = folder_path
        super().save(*args, **kwargs)

    def get_file_name(self):
        return os.path.basename(self.file.name)




# Получатель
class Recipient(models.Model):
    notice = models.ForeignKey('Notice', on_delete=models.CASCADE, verbose_name="Уведомление", related_name='recipient')
    name = models.CharField("Наименование", max_length=255)
    country = models.CharField("Страна", max_length=2)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return f"{self.name} ({self.country})"




 # Таблица на логи
# Действия пользователя - новая таблица для отслеживание логов по пользователям
# Логирование на каждое действие добавлять лог на пользваоетля что делал!!
class UserActionLog(models.Model):
    ACTION_TYPES = [
        ('create', 'Создание'),
        ('update', 'Обновление'),
        ('delete', 'Удаление'),
        ('close', 'Закрытие'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="Тип объекта", null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name="ID объекта", null=True, blank=True)
    action = models.CharField("Действие", max_length=20, choices=ACTION_TYPES)
    action_user = models.CharField("Описание действия пользователя", max_length=255, blank=True, null=True)
    description = models.TextField("Описание действия", blank=True, null=True)
    datetime = models.DateTimeField("Дата и время", default=now)

    class Meta:
        verbose_name = "Лог действия пользователя"
        verbose_name_plural = "Логи действий пользователей"

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} ({self.datetime})"




# Таблица регистраций со встрой БД, данные для заполнения берем с уведомлений
class EClient(models.Model):
    ideclient = models.AutoField(primary_key=True) # Первичный ключ (автоинкремент)
    regN_TS = models.CharField(max_length=25)      # Регистрационный номер ТС
    regN_DOK = models.CharField(max_length=45)     # Регистрационный номер документа
    countKod = models.IntegerField()               # Код количества - 0 всегда
    guidXML = models.CharField(max_length=42)      # GUID XML
    lc = models.DateTimeField(default=now)
    # lc = models.DateTimeField(auto_now_add=True)   # дата и время автоматически должно ставится
    id_us = models.IntegerField()                  # id usera будет всегда 68!
    id_z = models.IntegerField()                   # ID со своей таблицы order
    tip = models.IntegerField()                    # Тип регистрации - 4  ( уведомление )
    status = models.CharField(max_length=50)       # Статус сразу 0 - ставим "ожидание отправки", остальное присваиваться на регистрации
    regID = models.CharField(max_length=15)        # Номер регистрации
    numbEPI = models.CharField(max_length=100)     # Номер EPI
    statID = models.IntegerField()                 # ID статуса
    postIN = models.CharField(max_length=10)       # пост таможни наш 16466
    razr = models.CharField(max_length=45)         # Разрешение (всегда пусто)
    id_xmlf = models.IntegerField()                # ID XML файла (всегда 0 )

    def get_local_lc(self):
        """Возвращает lc в локальном часовом поясе"""
        return localtime(self.lc)  # Преобразует UTC в Europe/Minsk

    class Meta:
        managed = False  # Django не будет управлять структурой таблицы
        db_table = 'eclient'  # Имя таблицы в базе данных
        app_label = 'core'