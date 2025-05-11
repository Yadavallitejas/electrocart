from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')  # Display cart ID and date added in the admin panel

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')

    
admin.site.register(Cart, CartAdmin)  # Register the Cart model with the CartAdmin class
admin.site.register(CartItem, CartItemAdmin)  # Register the CartItem model with the CartItemAdmin class