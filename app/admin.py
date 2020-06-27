from django.contrib import admin
from .models import Item, Size, Flavor, Option

admin.site.register(Item)
admin.site.register(Size)
admin.site.register(Flavor)
admin.site.register(Option)