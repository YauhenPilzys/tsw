# Generated by Django 4.1 on 2025-02-19 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_carrier_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='product',
            name='recipient',
        ),
        migrations.AlterField(
            model_name='product',
            name='notice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='core.notice'),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
