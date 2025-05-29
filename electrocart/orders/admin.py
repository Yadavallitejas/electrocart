from django.contrib import admin
from .models import Order, OrderProduct, payment

# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'product_price', 'ordered','user', 'payment')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'email', 'city', 'state', 'order_total', 'tax', 'is_ordered')
    list_filter = ('status', 'is_ordered',)
    search_fields = ('order_number', 'full_name', 'phone', 'email')
    list_per_page = 20 
    inlines = [OrderProductInline]


admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(payment)