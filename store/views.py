from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id  # Import the _cart_id function from the cart views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator for pagination
from django.db.models import Q  # Import Q for complex queries
from .forms import ReviewForm  # Import the ReviewForm for submitting reviews
from .models import ReviewRating, ProductGallery  # Import ReviewRating and ProductGallery models
from django.contrib import messages  # Import messages for user feedback
from django.shortcuts import redirect  # Import redirect for redirecting after form submission
from orders.models import OrderProduct  # Import OrderProduct model to check if the product has been ordered by the user




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

    except Exception as e:
        raise e  # Raise any exceptions that 
    if request.user.is_authenticated:  # Check if the user is authenticated
        try:
            orderedproducts = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()  # Fetch ordered products for the single product
        except OrderProduct.DoesNotExist:
            orderedproducts = None
    else:
        orderedproducts = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)  # Fetch reviews for the single product

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)  # Fetch product gallery images for the single product

    context = {
        'single_product': single_product,  # Pass the single product to the template
        'in_cart': in_cart,  # Pass the in_cart status to the template
        'orderedproducts': orderedproducts,  # Pass the ordered
        'reviews': reviews,
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

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Get the URL of the previous page
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)  # Create a new ReviewRating object
            form = ReviewForm(request.POST, instance=reviews)  # Use the existing review instance
            form.save()  # Save the updated review
            messages.success(request, 'Thank you! Your review has been updated.')  # Show success message
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)  # Create a new ReviewForm instance
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)