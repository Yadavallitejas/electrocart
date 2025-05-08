from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    categories = None  # Initialize categories to None
    products = None  # Initialize products to None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)  # Fetch the category based on the slug
        products = Product.objects.filter(category=categories, available=True)
        product_count = products.count()  # Fetch products in the category that are available
    else:
        products = Product.objects.all().filter(available=True)  # Fetch all available products
        product_count = products.count()  # Count the number of products

    context = {
        'products': products,  # Pass the products to the template
        'categories': categories,  # Pass the categories to the template
        'product_count': product_count,  # Pass the product count to the template
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)  # Fetch the product based on category and product slug
    except Exception as e:
        raise e  # Raise any exceptions that occur

    context = {
        'single_product': single_product,  # Pass the single product to the template
    }
    return render(request, 'store/product_details.html', context)  # Render the product detail template with the context