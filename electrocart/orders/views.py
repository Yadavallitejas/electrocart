from django.shortcuts import render
from django.shortcuts import redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .models import Order
import datetime


def payments(request):
    return render(request, 'orders/payments.html')
# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity = cart_item.quantity
    tax = (2 * total) / 100

    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        print("Form is valid:", form.is_valid())
        if form.is_valid():
            data = form.save(commit=False)
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.user = current_user
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id)
            data.order_number = order_number

            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context ={
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'quantity': quantity,
            }
            return render(request, 'orders/payments.html', context)
        else:
            print("Form errors:", form.errors)
            from cart.views import checkout
            return checkout(request)
    else:
        return redirect('checkout')

