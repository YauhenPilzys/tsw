# Generated by Django 5.1.3 on 2025-01-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_notice_unp_alter_order_status_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='unp',
            field=models.CharField(default='591489147', editable=False, max_length=9, verbose_name='УНП компании'),
        ),
    ]
