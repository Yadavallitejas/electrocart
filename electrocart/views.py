from django.shortcuts import render
from category.models import Category
from store.models import Product

from store.models import ReviewRating

def home(request):
    products = Product.objects.filter(available=True).order_by('?')[:6]
    categories = Category.objects.all()
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {
        'products': products,
        'categories': categories,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)
