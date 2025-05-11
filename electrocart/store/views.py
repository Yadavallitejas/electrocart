from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id  # Import the _cart_id function from the cart views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator for pagination
from django.db.models import Q  # Import Q for complex queries


# Create your views here.
def store(request, category_slug=None):
    categories = None  # Initialize categories to None
    products = None  # Initialize products to None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)  # Fetch the category based on the slug
        products = Product.objects.filter(category=categories, available=True)
        product_count = products.count()  # Fetch products in the category that are available
        paginator = Paginator(products, 3)  # Create a paginator object with 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page
    else:
        products = Product.objects.all().filter(available=True).order_by('id')  # Fetch all available products
        product_count = products.count()  # Count the number of products
        paginator = Paginator(products, 3)  # Create a paginator object with 6 products per page
        page = request.GET.get('page')  # Get the current page number from the request
        paged_products = paginator.get_page(page)  # Get the products for the current page

    context = {
        'products': paged_products,  # Pass the products to the template
        'categories': categories,  # Pass the categories to the template
        'product_count': product_count,  # Pass the product count to the template
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    from .models import Variation
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)  # Fetch the product based on category and product slug
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  # Check if the product is in the cart

        # Fetch color and size variations for the product
        colors = Variation.objects.colors().filter(product=single_product)
        sizes = Variation.objects.sizes().filter(product=single_product)

        # Attach variations to the product object for template access
        single_product.colors = colors
        single_product.sizes = sizes

    except Exception as e:
        raise e  # Raise any exceptions that occur

    context = {
        'single_product': single_product,  # Pass the single product to the template
        'in_cart': in_cart,  # Pass the in_cart status to the template
    }
    return render(request, 'store/product_details.html', context)  # Render the product detail template with the context

def search(request):
    products = None  # Initialize products to None
    product_count = 0  # Initialize product count to 0

    
    if 'keyword' in request.GET:  # Check if 'keyword' is in the GET request
        keyword = request.GET['keyword']  # Get the keyword from the request
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) | (Q(product_name__icontains=keyword)))  # Filter products based on the keyword or product_name__icontains=keyword)  
            product_count = products.count()
        context = {
            'products': products,  # Pass the filtered products to the template
            'product_count': product_count,  # Pass the product count to the template
            'keyword': keyword,  # Pass the keyword to the template
        }
    return render(request, 'store/store.html', context)  # Render the store template with the filtered products
