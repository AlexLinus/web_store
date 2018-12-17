# Generated by Django 2.1.4 on 2018-12-12 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Итоговая сумма заказа'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True, verbose_name='Цена'),
        ),
    ]
