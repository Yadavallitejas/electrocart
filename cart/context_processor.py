from .models import Cart, CartItem
from .views import _cart_id  # Import the _cart_id function from the cart views

def counter(request):
    cart_count = 0  # Initialize cart count to 0
    if 'admin' in request.path:  # Check if the request path contains 'admin'
        return {}  # Return an empty dictionary if it does
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))  # Get the cart using the session key
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])  # Get the first cart item
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)  # Return the cart count as a context variable