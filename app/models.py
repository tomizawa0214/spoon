from django.conf import settings
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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
    size_image = models.ImageField('サイズ画像', upload_to='images')
    flavor_title = models.CharField('フレーバー', max_length=100)
    flavor_price = models.IntegerField('フレーバー価格', default=0)
    flavor_image = models.ImageField('フレーバー画像', upload_to='images')
    flavor2_title = models.CharField('フレーバー2', max_length=100, blank=True, null=True)
    flavor2_price = models.IntegerField('フレーバー2価格', default=0)
    flavor2_image = models.ImageField('フレーバー2画像', upload_to='images', blank=True, null=True)
    option_title = models.CharField('オプション', max_length=100, blank=True, null=True)
    option_price = models.IntegerField('オプション価格', default=0)
    option_image = models.ImageField('オプション画像', upload_to='images', blank=True, null=True)
    option2_title = models.CharField('オプション2', max_length=100, blank=True, null=True)
    option2_price = models.IntegerField('オプション2価格', default=0)
    option2_image = models.ImageField('オプション2画像', upload_to='images', blank=True, null=True)
    option3_title = models.CharField('オプション3', max_length=100, blank=True, null=True)
    option3_price = models.IntegerField('オプション3価格', default=0)
    option3_image = models.ImageField('オプション3画像', upload_to='images', blank=True, null=True)
    option4_title = models.CharField('オプション4', max_length=100, blank=True, null=True)
    option4_price = models.IntegerField('オプション4価格', default=0)
    option4_image = models.ImageField('オプション4画像', upload_to='images', blank=True, null=True)
    ordered = models.BooleanField('注文完了', default=False)

    def get_total_item_price(self):
        return self.size_price + self.flavor_price + self.flavor2_price + self.option_price + self.option2_price + self.option3_price + self.option4_price

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
    order_day = models.IntegerField('注文受取日')
    count = models.IntegerField('注文番号', default=0)
    flag = models.BooleanField(default=False)

    def get_total(self):
        total = 0
        for cart in self.cart.all():
            total += cart.get_total_item_price()
        return total

    def __str__(self):
        return f'{self.name}　{self.receipt}'


class TodayOrder(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(
            ('当日注文'),
            default=True,
            help_text=(
                '当日注文に対応するかを指定します。 '
                '選択を解除すると翌日以降の注文になります。'
            ),
        )
    
    def __str__(self):
        return self.name


class WhatsNew(models.Model):
    date = models.DateField('日付')
    comment = models.TextField(
        ('コメント'),
        max_length=45,
        help_text=(
            '※45文字以内で入力してください。'
        ),
    )

    def __str__(self):
        return self.comment


class PickUp(models.Model):
    e_name = models.CharField('英語名', max_length=100)
    j_name = models.CharField('日本語名', max_length=100)
    m_price = models.IntegerField('ミニ価格')
    s_price = models.IntegerField('シングル価格')
    w_price = models.IntegerField('ダブル価格')
    comment = models.TextField(
        ('コメント'),
        max_length=100,
        help_text=(
            '※100文字以内で入力してください。'
        ),
    )
    image = ProcessedImageField(
        verbose_name='画像',
        upload_to='images',
        processors=[ResizeToFill(600, 600)],
        options={'quality': 60}
    )

    def __str__(self):
        return self.j_name