from django.db import models
from django.utils import timezone


class Cart(models.Model):
    size_title = models.CharField('サイズ', max_length=100)
    size_price = models.CharField('サイズ価格', max_length=100)
    flavor_title = models.CharField('フレーバー', max_length=100)
    flavor_title_2 = models.CharField('フレーバー2', max_length=100)
    option_title = models.CharField('オプション', max_length=100)
    option_price = models.CharField('オプション価格', max_length=100)
    option_title_2 = models.CharField('オプション2', max_length=100)
    option_price_2 = models.CharField('オプション2価格', max_length=100)
    total_price = models.IntegerField('合計', default=0)

    def __str__(self):
        return self.size_title


class Order(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='予約注文商品', on_delete=models.DO_NOTHING)
    name = models.CharField('お名前', max_length=30)
    furigana = models.CharField('フリガナ', max_length=30)
    email = models.EmailField('メールアドレス', max_length=256)
    tel = models.CharField('電話番号', max_length=13)
    receipt = models.CharField('受取日時', max_length=30)
    created = models.DateTimeField('注文受付日', default=timezone.now)

    def __str__(self):
        return f'{self.name} {self.created}'


class Size(models.Model):
    title = models.CharField('サイズ', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class Flavor(models.Model):
    title = models.CharField('フレーバー', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class Option(models.Model):
    title = models.CharField('オプション', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title