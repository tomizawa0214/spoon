# Generated by Django 2.2.12 on 2020-08-11 01:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20200803_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default=False, help_text='受け取りが完了したら選択 ', verbose_name='受け取り'),
        ),
        migrations.AddField(
            model_name='order',
            name='standby',
            field=models.BooleanField(default=False, help_text='商品の準備が完了したら選択 ', verbose_name='準備'),
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon_day',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='クーポン利用日'),
        ),
        migrations.AlterField(
            model_name='order',
            name='receipt',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='受取日時'),
        ),
    ]
