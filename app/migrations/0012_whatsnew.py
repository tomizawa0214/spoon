# Generated by Django 2.2.12 on 2020-07-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20200716_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('comment', models.CharField(help_text='※48文字以内で入力してください。', max_length=48, verbose_name='コメント')),
            ],
        ),
    ]
