from django.contrib import admin
from .models import Product, User, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
