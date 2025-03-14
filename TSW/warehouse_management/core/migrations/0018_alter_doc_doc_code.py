# Generated by Django 4.1 on 2025-02-20 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_product_customer_remove_product_recipient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='doc_code',
            field=models.CharField(choices=[('02013', 'Железнодорожная накладная'), ('02014', 'Иные документы, предусмотренные правилами перевозки по железной дороге'), ('02015', 'Транспортная накладная, предусмотренная Конвенцией о договоре международной дорожной перевозки грузов 1956 года'), ('02016', 'Иная транспортная накладная, используемая при перевозке товаров автодорожным транспортом\t'), ('02024', 'Книжка МДП'), ('02025', 'Карнет АТА'), ('04021', 'Счет-фактура (инвойс) к договору'), ('04025', 'Счет-проформа к договору '), ('04131', 'Отгрузочный (упаковочный) лист'), ('04023', 'Банковские документы, а также другие платежные документы, отражающие стоимость товара'), ('03011', 'Договор (контракт), заключенный при совершении сделки с товарами'), ('09013', 'Транзитная декларация'), ('09035', 'Декларация на товары'), ('09999', 'Иные транспортные документы')], max_length=5, verbose_name='Код документа'),
        ),
    ]
