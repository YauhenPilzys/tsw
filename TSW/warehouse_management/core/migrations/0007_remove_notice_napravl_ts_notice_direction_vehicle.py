# Generated by Django 4.1 on 2025-02-04 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_notice_gross_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='napravl_ts',
        ),
        migrations.AddField(
            model_name='notice',
            name='direction_vehicle',
            field=models.CharField(choices=[('1', 'Вывоз c территории РБ'), ('2', 'Ввоз на территорию РБ')], default='2', max_length=1, verbose_name='Направление т/с'),
        ),
    ]
