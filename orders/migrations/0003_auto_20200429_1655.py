# Generated by Django 3.0.5 on 2020-04-29 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200428_2152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinorder',
            options={'verbose_name': 'Товар заказа', 'verbose_name_plural': 'Товары заказа'},
        ),
    ]
