from django.conf import settings
from django.db import models
from django.utils import timezone


class SizeItem(models.Model):
    title = models.CharField('名称', max_length=100)
    price = models.IntegerField('価格')
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class FlavorItem(models.Model):
    entitle = models.CharField('英語名称', max_length=100)
    title = models.CharField('日本語名称', max_length=100)
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
    title = models.CharField('名称', max_length=100)
    price = models.IntegerField('価格', default=0)
    image = models.ImageField('画像', upload_to='images')

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    size_title = models.CharField('サイズ', max_length=100)
    size_price = models.IntegerField('サイズ価格')
    flavor_title = models.CharField('フレーバー', max_length=100)
    flavor_price = models.IntegerField('フレーバー価格', default=0)
    flavor2_title = models.CharField('フレーバー2', max_length=100, blank=True, null=True)
    flavor2_price = models.IntegerField('フレーバー2価格', default=0)
    option_title = models.CharField('オプション', max_length=100, blank=True, null=True)
    option_price = models.IntegerField('オプション価格', default=0)
    option2_title = models.CharField('オプション2', max_length=100, blank=True, null=True)
    option2_price = models.IntegerField('オプション2価格', default=0)
    option3_title = models.CharField('オプション3', max_length=100, blank=True, null=True)
    option3_price = models.IntegerField('オプション3価格', default=0)
    total_price = models.IntegerField('合計')
    ordered = models.BooleanField('注文完了', default=False)

    def __str__(self):
        return f'{self.user.name}　{self.size_title}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart, verbose_name='カート')
    name = models.CharField('お名前', max_length=30)
    furigana = models.CharField('フリガナ', max_length=30)
    email = models.EmailField('メールアドレス', max_length=256)
    tel = models.CharField('電話番号', max_length=13)
    receipt = models.CharField('受取日時', max_length=30)
    created = models.DateTimeField('注文日時', default=timezone.now)

    def __str__(self):
        return f'{self.name}　{self.receipt}'