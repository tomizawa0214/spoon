from django.contrib import admin
from .models import Order, Cart, Size, Flavor, Option, Item

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Size)
admin.site.register(Flavor)
admin.site.register(Option)
admin.site.register(Item)