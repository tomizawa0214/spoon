from django.db import models


class Cart(models.Model):
    size_title = models.CharField(verbose_name='サイズ', max_length=100)
    size_price = models.CharField(verbose_name='サイズ価格', max_length=100)
    flavor_title = models.CharField(verbose_name='フレーバー', max_length=100)
    flavor_title_2 = models.CharField(verbose_name='フレーバー2', max_length=100)
    option_title = models.CharField(verbose_name='オプション', max_length=100)
    option_price = models.CharField(verbose_name='オプション価格', max_length=100)
    option_title_2 = models.CharField(verbose_name='オプション2', max_length=100)
    option_price_2 = models.CharField(verbose_name='オプション2価格', max_length=100)
    total_price = models.IntegerField(verbose_name='合計', default=0)

    def __str__(self):
        return self.size_title


class Size(models.Model):
    title = models.CharField(verbose_name='サイズ', max_length=100)
    price = models.IntegerField(verbose_name='価格', default=0)
    image = models.ImageField(verbose_name='画像', upload_to='images')

    def __str__(self):
        return self.title


class Flavor(models.Model):
    title = models.CharField(verbose_name='フレーバー', max_length=100)
    price = models.IntegerField(verbose_name='価格', default=0)
    image = models.ImageField(verbose_name='画像', upload_to='images')

    def __str__(self):
        return self.title


class Option(models.Model):
    title = models.CharField(verbose_name='オプション', max_length=100)
    price = models.IntegerField(verbose_name='価格', default=0)
    image = models.ImageField(verbose_name='画像', upload_to='images')

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