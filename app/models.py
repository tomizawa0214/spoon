from django.conf import settings
from django.db import models
from django.utils import timezone


# class OrderHistory(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     size_title = models.CharField('サイズ', max_length=100)
#     size_price = models.CharField('サイズ価格', max_length=100)
#     flavor_title = models.CharField('フレーバー', max_length=100)
#     flavor_title_2 = models.CharField('フレーバー2', max_length=100, blank=True, null=True)
#     option_title = models.CharField('オプション', max_length=100, blank=True, null=True)
#     option_price = models.CharField('オプション価格', max_length=100, blank=True, null=True)
#     option_title_2 = models.CharField('オプション2', max_length=100, blank=True, null=True)
#     option_price_2 = models.CharField('オプション2価格', max_length=100, blank=True, null=True)
#     total_price = models.IntegerField('合計')
#     created = models.DateTimeField('登録日', default=timezone.now)

#     def __str__(self):
#         return f'{self.size_title}　{self.created}'


# class Order(models.Model):
#     name = models.CharField('お名前', max_length=30)
#     furigana = models.CharField('フリガナ', max_length=30)
#     email = models.EmailField('メールアドレス', max_length=256)
#     tel = models.CharField('電話番号', max_length=13)
#     receipt = models.CharField('受取日時', max_length=30)
#     created = models.DateTimeField('注文受付日', default=timezone.now)

#     def __str__(self):
#         return f'{self.name}　{self.created}'


# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     size_title = models.CharField('サイズ', max_length=100)
#     size_price = models.CharField('サイズ価格', max_length=100)
#     flavor_title = models.CharField('フレーバー', max_length=100)
#     flavor_title_2 = models.CharField('フレーバー2', max_length=100, blank=True, null=True)
#     option_title = models.CharField('オプション', max_length=100, blank=True, null=True)
#     option_price = models.CharField('オプション価格', max_length=100, blank=True, null=True)
#     option_title_2 = models.CharField('オプション2', max_length=100, blank=True, null=True)
#     option_price_2 = models.CharField('オプション2価格', max_length=100, blank=True, null=True)
#     total_price = models.IntegerField('合計')

#     def __str__(self):
#         return self.size_title


class SizeItem(models.Model):
    title = models.CharField('サイズ', max_length=100)
    price = models.IntegerField('価格')
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class FlavorItem(models.Model):
    title = models.CharField('フレーバー', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')
    is_active = models.BooleanField(
            ('掲載判定'),
            default=True,
            help_text=(
                'このフレーバーを掲載するかを指定します。 '
                '選択を解除すると非表示になります。'
            ),
        )

    def __str__(self):
        return self.title


class OptionItem(models.Model):
    title = models.CharField('オプション', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    size_item = models.ForeignKey(SizeItem, on_delete=models.CASCADE)
    flavor_item = models.ManyToManyField(FlavorItem)
    option_item = models.ManyToManyField(OptionItem)

    def get_total_item_price(self):
        return self.size_item.price + self.flavor_item.price + self.option_item.price

    def __str__(self):
        return self.user.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def __str__(self):
        return self.user.name