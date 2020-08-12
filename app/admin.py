from django.contrib import admin
from .models import PickUp, WhatsNew, TodayOrder, Order, Cart, SizeItem, FlavorItem, OptionItem

class StandbyListFilter(admin.SimpleListFilter):
    title = '注文の準備'
    parameter_name = 'standby'

    def lookups(self, request, model_admin):
        return (
            ('True', '準備OK'),
            ('False', '準備まだ')
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(standby=True)
        elif self.value() == 'False':
            return queryset.filter(standby=False)
        else:
            return queryset.all()


class CompleteListFilter(admin.SimpleListFilter):
    title = '受け取り済み'
    parameter_name = 'complete'

    def lookups(self, request, model_admin):
        return (
            ('True', '受け取り済み'),
            ('False', 'まだ来てない')
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(complete=True)
        elif self.value() == 'False':
            return queryset.filter(complete=False)
        else:
            return queryset.all()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'furigana', 'order_number', 'receipt_datetime', 'standby', 'complete')
    ordering = ('receipt',)
    list_filter = (StandbyListFilter, CompleteListFilter)
    list_editable = ('standby', 'complete')


class TodayOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)


class SizeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


class FlavorItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')
    list_editable = ('is_active',)


class OptionItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


admin.site.register(PickUp)
admin.site.register(WhatsNew)
admin.site.register(TodayOrder, TodayOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(SizeItem, SizeItemAdmin)
admin.site.register(FlavorItem, FlavorItemAdmin)
admin.site.register(OptionItem, OptionItemAdmin)
