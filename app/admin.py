from django.contrib import admin
from .models import Cart, Size, Flavor, Option, Item

admin.site.register(Cart)
admin.site.register(Size)
admin.site.register(Flavor)
admin.site.register(Option)
admin.site.register(Item)