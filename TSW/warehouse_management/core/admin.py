from django.utils.html import mark_safe
from django.contrib import admin
from .models import (
    TSW, Warehouse, Product, Ramp, Place, TypePlace, ServiceOrder,
    Transfer, Order, Parking, PlacePark, Supplier, LogBook, Notice, Doc, LogPlace, Recipient, TransportNotice, Transport, DocumentFile, Pallet
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku_product", "type_product", "quantity", "place", "show_barcode")
    readonly_fields = ("barcode_image", "show_barcode")

    def show_barcode(self, obj):
        if obj.barcode_image:
            return mark_safe(f'<img src="{obj.barcode_image.url}" width="150" height="150" />')
        return "Нет штрихкода"

    show_barcode.short_description = "Штрихкод"


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    list_display = ("sku_pallet", "place", "current_weight", "show_barcode")
    readonly_fields = ("barcode_image", "show_barcode")

    def show_barcode(self, obj):
        if obj.barcode_image:
            return mark_safe(f'<img src="{obj.barcode_image.url}" width="150" height="150" />')
        return "Нет штрихкода"

    show_barcode.short_description = "Штрихкод паллеты"


admin.site.register(TSW)  # Склад временного хранения
admin.site.register(Warehouse)  # Склад
admin.site.register(Ramp)  # Рампа
# admin.site.register(Product)  # Товар
admin.site.register(LogPlace)  # Перемещение товара по местам
admin.site.register(Place)  # Место складирования
admin.site.register(TypePlace)  # Тип места
admin.site.register(ServiceOrder)  # Заказ услуги
admin.site.register(Transfer)  # Передача груза
admin.site.register(Order)  # Заказ
admin.site.register(Parking)  # Парковка
admin.site.register(PlacePark)  # Парковочное место
admin.site.register(Supplier)  # Поставщик
admin.site.register(LogBook)  # Журнал въезда/выезда
admin.site.register(Notice)  # Уведомление
admin.site.register(Transport)  # Транспорт
admin.site.register(TransportNotice)  # Транспорт-Уведомление
admin.site.register(Doc)  # Документы
admin.site.register(DocumentFile)  # Файлы документа
# admin.site.register(ActionLog)  # Логи действий
admin.site.register(Recipient)  # Получатель