from django.db import models
from store.models import Product  # Import the Product model from the store app

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)  # Unique identifier for the cart
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp for when the cart was created

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Foreign key referencing the Productioo
    variations = models.ManyToManyField('store.Variation', blank=True)  # Many-to-many relationship with Variation
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Foreign key referencing the Cart
    quantity = models.IntegerField()  # Quantity of the product in the cart
    is_active = models.BooleanField(default=True)  # Indicates if the item is active in the cart

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} - Quantity: {self.quantity}"
    