# Generated by Django 2.1.4 on 2018-12-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20181223_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Выполняется', 'Выполняется'), ('Оплачен', 'Оплачен'), ('Принят в обработку', 'Принят в обработку')], default='Принят в обработку', max_length=100),
        ),
    ]
