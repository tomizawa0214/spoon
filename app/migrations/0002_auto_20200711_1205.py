# Generated by Django 2.2.12 on 2020-07-11 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(to='app.Cart', verbose_name='カート'),
        ),
    ]
