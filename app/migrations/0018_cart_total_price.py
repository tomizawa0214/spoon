# Generated by Django 2.2.12 on 2020-06-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='合計'),
        ),
    ]
