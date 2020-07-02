from django.db import models


# class OrderUser(models.Model):
#     name = models.CharField('お名前', max_length=30)
#     email = models.EmailField('メールアドレス', min_length=7, max_length=256)
#     phone = models.CharField('電話番号', min_length=10, max_length=11)
#     receipt = models.DateTimeField('受取希望日時', default=timezone.now)

#     def __str__(self):
#         receipt = timezone.localtime(self.receipt).strftime('%Y/%m/%d %H:%M')
#         return f'{self.name}{receipt}'


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