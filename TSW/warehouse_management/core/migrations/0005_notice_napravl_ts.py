# Generated by Django 4.1 on 2025-02-04 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_doc_doc_code_alter_notice_purpose_placement'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='napravl_ts',
            field=models.CharField(choices=[('1', 'Вывоз c территорию РБ'), ('2', 'Ввоз на территорию РБ')], default='2', max_length=1, verbose_name='Направление т/с'),
        ),
    ]
