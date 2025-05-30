from django.shortcuts import render
from django.shortcuts import redirect
from cart.models import Cart, CartItem
from .forms import OrderForm
from .models import Order, payment, OrderProduct 
import datetime
import json
from store.models import Product, Variation
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = payment(
        user=request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']

         
     )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = orderproduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()


        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    CartItem.objects.filter(user=request.user).delete()

    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)  
        
    
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

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        payment = payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment, 
            'subtotal': subtotal,          
        }
        return render(request, 'orders/order_complete.html', context)
    except (payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


