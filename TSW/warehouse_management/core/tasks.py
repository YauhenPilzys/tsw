# from .reg_func import *
# import logging
# from .models import *
# import json
# from django.utils import timezone
# from datetime import timedelta
# import urllib3
#
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # отключаем сообщения Warrings, что имеется HTTP-запрос без проверки SSL-сертификата
#
# logger = logging.getLogger('main')
# env = environ.Env(
#     DEBUG=(bool, False)
# )
#
# """
# обновление статусов регистраций с насэд записей из БД за последние 12 часов
# 1) проверяем, есть ли записи, которые стоит обновить за сегодняшний день по статусу
# 2) если такие записи есть, то делаем запрос в насед по 70 последним записям
# 3) сопоставляем по GUID записи и обновляем статус
# """
#
#
# def update_reg_status():  # обновление статусов раз в 2-3 мин
#     # logger.info('update_reg_status')
#     # print('update_reg_status')
#     # Получаем текущее время
#     now = timezone.now()
#     # Вычисляем время 12 часов назад
#     t12 = now - timedelta(hours=12)
#     # берем те, в которые надо обновить статус - отправлена, передана, обрабатывается, но за последние 12 часов
#     r = Registration.objects.filter(Status__in=['-1', '0', '1'], DateTime__gte=t12)
#     count_reg = 0  # запоминаем сколько записей нужно проверить count_reg = r.count() - значит проверили все записи
#     if r is not None:
#         # делаем запрос в насед
#         n = get_nased('range', 0, 70)
#         if (n is not None) and (n.strip() != ""):
#             try:
#                 d = json.loads(n)
#                 for i in d['requests']:
#                     # идем по выбранным записям из БД
#                     for j in r:
#                         if i['file_guid'] == j.GUID:
#                             # обновляем данные
#                             j.Status = i['status_id']
#                             j.RegID = ''
#                             j.RegNumber = ''
#                             j.RegDate = ''
#                             j.Permit = ''
#                             if (j.RegID == '') or (j.RegID is None):
#                                 j.RegID = i['id']
#                             if (j.RegNumber == '') or (j.RegNumber is None):
#                                 j.RegNumber = i['reg_no']
#                             if (j.RegDate == '') or (j.RegDate is None):
#                                 j.RegDate = i['date_reg']
#                             if (j.Permit == '') or (j.Permit is None):
#                                 j.Permit = i['app_no']
#                             count_reg += 1
#                             j.save()
#                             # также одновременно обновляем поля в заказе
#                             o = j.OrderID
#                             if j.GUID == i['file_guid']:  # если гуид в заказе такой же
#                                 o.Status_ = i['status_id']
#                                 o.RegNumber = i['reg_no']
#                                 o.save()
#             except json.JSONDecodeError:
#                 print("Ошибка: n не является корректным JSON")
#
#     else:
#         return 0  # Нет записей для обновления статуса в таблице Registration
#
#
# def update_reg_status_2days():  # обновление статусов раз в 2 дня всех, которые остались - по GUID
#     # logger.info('update_reg_status')
#     # print('update_reg_status')
#     # берем те, в которые надо обновить статус - отправлена, передана, обрабатывается
#     r = Registration.objects.filter(Status__in=['-1', '0', '1'])
#     count_reg = 0  # запоминаем сколько записей нужно проверить count_reg = r.count() - значит проверили все записи
#     if r is not None:
#         for j in r:
#             # делаем запрос в насед
#             n = get_nased('guid', j.GUID)
#             if (n is not None) and (n.strip() != ""):
#                 try:
#                     d = json.loads(n)
#                     for i in d['requests']:
#                         if i['file_guid'] == j.GUID:
#                             # обновляем данные
#                             j.Status = i['status_id']
#                             # j.RegID = ''
#                             # j.RegNumber = ''
#                             # j.RegDate = ''
#                             # j.Permit = ''
#                             if (j.RegID == '') or (j.RegID is None):
#                                 j.RegID = i['id']
#                             if (j.RegNumber == '') or (j.RegNumber is None):
#                                 j.RegNumber = i['reg_no']
#                             if (j.RegDate == '') or (j.RegDate is None):
#                                 j.RegDate = i['date_reg']
#                             if (j.Permit == '') or (j.Permit is None):
#                                 j.Permit = i['app_no']
#                             count_reg += 1
#                             j.save()
#                             # также одновременно обновляем поля в заказе
#                             o = j.OrderID
#                             if j.GUID == i['file_guid']:  # если гуид в заказе такой же
#                                 o.Status_reg = i['status_id']
#                                 o.RegNumber = i['reg_no']
#                                 # если уведомление не в статусе регистрации
#                                 if (o.Status_reg not in ['-1', '0', '1']):
#                                     o.Status = '2'  # отправлен
#                                     o.save()
#                                 # если уведомление снято с контроля и счет выписан - 14 статус по регистрации
#                                 b = Bills.objects.filter(OrderID=o).first()
#                                 if (b is None):  # значит счет выписан
#                                     if (o.Status_reg == '14'):
#                                         o.Status = '4'  # заказ закрыт
#                                         o.save()
#                 except json.JSONDecodeError:
#                     print("Ошибка: n не является корректным JSON")
#
#     else:
#         return 0  # Нет записей для обновления статуса в таблице Registration
