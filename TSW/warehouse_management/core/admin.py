from django.contrib import admin
from .models import (
    TSW, Warehouse, Product, Ramp, Place, TypePlace, ServiceOrder,
    Transfer, Order, Parking, PlacePark, Supplier, LogBook, Notice, Doc, LogPlace, Recipient, TransportNotice, Transport
)


#Регистрация всех моделей в админке
# @admin.register(ActionLog)
# class ActionLogAdmin(admin.ModelAdmin):
#     list_display = ('user', 'content_type', 'object_id', 'action', 'datetime')
#     list_filter = ('user', 'content_type', 'action', 'datetime')
#     search_fields = ('user__username', 'action', 'object_id')

admin.site.register(TSW)  # Склад временного хранения
admin.site.register(Warehouse)  # Склад
admin.site.register(Ramp)  # Рампа
admin.site.register(Product)  # Товар
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
# admin.site.register(ActionLog)  # Логи действий
admin.site.register(Recipient)  # Получатель




# @admin.register(TSW)
# class TSWAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#
#
# @admin.register(Warehouse)
# class WarehouseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'address', 'note')
#     list_filter = ('name',)
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'sku', 'type_product', 'quantity', 'datetime_in', 'datetime_out')
#     list_filter = ('type_product',)
#
#
# @admin.register(Ramp)
# class RampAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description', 'status_ramp', 'note')
#     list_filter = ('status_ramp',)
#
#
# @admin.register(Place)
# class PlaceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'type_place', 'status_place', 'characteristic', 'note')
#     list_filter = ('status_place',)
#
#
# @admin.register(TypePlace)
# class TypePlaceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description', 'max_weight', 'max_size', 'type_place')
#
#
# @admin.register(ServiceOrder)
# class ServiceOrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description_service', 'price', 'price_nds', 'currency')
#
#
# @admin.register(Transfer)
# class TransferAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'order_in', 'order_out', 'quantity', 'price', 'type_transfer', 'is_fully_transferred')
#     list_filter = ('type_transfer',)
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'number_notification', 'warehouse', 'supplier', 'status_order', 'datetime', 'carrier_name', 'user')
#     list_filter = ('status_order', 'damage')
#
#
# @admin.register(Parking)
# class ParkingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'warehouse', 'description', 'note')
#
#
# @admin.register(PlacePark)
# class PlaceParkAdmin(admin.ModelAdmin):
#     list_display = ('id', 'parking', 'spot_number', 'size', 'is_available')
#
#
# @admin.register(Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'city', 'phone', 'tax_number')
#
#
# @admin.register(LogBook)
# class LogBookAdmin(admin.ModelAdmin):
#     list_display = ('id', 'warehouse', 'status', 'carrier_info', 'datetime_in', 'datetime_out')
#     list_filter = ('status', 'removed_control')
#
#
# @admin.register(Notice)
# class NoticeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'doc_creation_date', 'order', 'truck', 'gross_weight')
#     list_filter = ('truck_country',)
#
#
# @admin.register(Doc)
# class DocAdmin(admin.ModelAdmin):
#     list_display = ('id', 'notice', 'doc_code', 'doc_number', 'doc_date')
#     list_filter = ('doc_code',)
#
#
# @admin.register(LogPlace)
# class LogPlaceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'place_from', 'place_to', 'quantity', 'datetime', 'user', 'note')
#     list_filter = ('product',)
#
#
# @admin.register(ActionLog)
# class ActionLogAdmin(admin.ModelAdmin):
#     list_display = ['user', 'action', 'datetime']
#     list_filter = ['datetime', 'user']
#
#
# @admin.register(Recipient)
# class RecipientAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'country')
#     search_fields = ('name', 'country')
