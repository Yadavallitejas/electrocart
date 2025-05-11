from django.shortcuts import render, redirect
from .models import Cart, CartItem  # Import the Cart and CartItem models
from store.models import Product, Variation  # Import the Product model from the store app
from django.http import HttpResponse  # Import HttpResponse for returning responses
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist for exception handling


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key  # Get the session key for the cart
    if not cart:
        cart = request.session.create()  # Create a new session if it doesn't exist
    return cart

def add_cart(request, product_id):
    product_variation = []  # Initialize an empty list for product variations

    product = Product.objects.get(id=product_id)  # Get the product by ID

    if request.method == 'POST':

        for item in request.POST:
            key = item  # Get the key from the POST request
            value = request.POST[item]  # Get the value from the POST request
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)  # Get the variation based on the product and key-value pair
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))  # Create a new cart if it doesn't exist
    cart.save()  # Save the cart
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()  # Check if the cart item already exists

    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product,cart=cart)  # Get the cart items queryset
        ex_var_list = []  # Initialize an empty list for existing variations
        id = []
        for item in cart_items:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)  # Append the ID of the cart item to the list

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]  # Get the ID of the existing cart item
            item = CartItem.objects.get(product=product, id=item_id)  # Get the cart item by product and ID
            item.quantity += 1  # Increment the quantity
            item.save()  # Save the updated cart item

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)  # Create a new cart item
            if len(product_variation) > 0:
                item.variations.clear()  # Clear the existing variations
                
                item.variations.add(*product_variation)  # Add the new variations to the cart item
            item.save()  # Save the updated cart item
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)  # Create a new cart item
        if len(product_variation) > 0:
            cart_item.variations.clear()  # Clear the existing variations
            cart_item.variations.add(*product_variation)  # Add the new variations to the cart item
        cart_item.save()  # Save the new cart item


    return redirect('cart')  # Redirect to the cart page

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
    product = Product.objects.get(id=product_id)  # Get the product by ID
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)  # Get the cart item by id
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrement the quantity
            cart_item.save()  # Save the updated cart item
        else:
            cart_item.delete()  # Delete the cart item if quantity is 1
    except:
        pass  # If the cart item does not exist, do nothing
    

    return redirect('cart')  # Redirect to the cart page

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
    product = Product.objects.get(id=product_id)  # Get the product by ID
    cart_item = CartItem.objects.get(product=product, cart=cart)  # Get the cart item
    cart_item.delete()  # Delete the cart item

    return redirect('cart')  # Redirect to the cart page


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Get active cart items
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity  # Calculate total quantity
        tax = (5 * total)/100  # Calculate tax (5% of total)
        grand_total = total + tax  # Calculate grand total
    except Cart.DoesNotExist:
        pass  # If the cart does not exist, do nothing

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,  # Pass the cart items to the template
        'tax': tax,
        'grand_total': grand_total

    }
    return render(request, 'store/cart.html', context)  # Render the cart template
