from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='photos/products', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
class variation_manager(models.Manager):
    def colors(self):
        return super(variation_manager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(variation_manager, self).filter(variation_category='size', is_active=True)
    
variation_category_choices = {
    ('color', 'color'),
    ('size', 'size'),
}
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=255, choices=variation_category_choices)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = variation_manager()

    def __str__(self):
        return self.variation_value
