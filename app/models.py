from django.db import models


class Size(models.Model):
    title = models.CharField('サイズ', max_length=10)
    price = models.IntegerField('価格', null=True)
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

# FLAVOR_CHOICES = (
#     ('バニラ', 'バニラ'),
#     ('マンゴー', 'マンゴー'),
#     ('オレンジ', 'オレンジ'),
# )

# OPTION_CHOICES = (
#     ('コーン', 'コーン'),
#     ('ドライアイス', 'ドライアイス'),
# )

# class Order(models.Model):
#     size = models.CharField ("サイズ", max_length=10, choices=SIZE_CHOICES, blank=True)
#     flavor = models.CharField ('フレーバー', max_length=50, choices=FLAVOR_CHOICES, blank=True)
#     option = models.CharField ('オプション', max_length=10, choices=OPTION_CHOICES, blank=True)

#     def __str__(self):
#         return self.size

