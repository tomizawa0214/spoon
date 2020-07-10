from django.contrib import admin
from .models import OrderItem, Order, SizeItem, FlavorItem, OptionItem

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(SizeItem)
admin.site.register(FlavorItem)
admin.site.register(OptionItem)