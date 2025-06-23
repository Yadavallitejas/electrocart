from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserForm, UserProfileform
from .models import account
from orders.models import Order
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from cart.models import Cart, CartItem
from cart.views import _cart_id
import requests
from django.shortcuts import get_object_or_404
from .models import UserProfile
from orders.models import OrderProduct


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = email.split('@')[0]
            user = account.objects.create_user(first_name=first_name, last_name=last_name, username=user_name , email=email, password=password, phone_number=phone_number)
            user.phone_number = phone_number
            user.save()
            # You might want to redirect after successful registration
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, "Thankyou for registering, we have sent you a verification email. Please verify your account your account.")
            return redirect('/accounts/login/?command=verification&email='+email)

        else:
            # Form is invalid, render the form with errors
            context = {'form': form}
            return render(request, 'accounts/register.html', context)
    else:
        form = RegistrationForm()

 
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the session key
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)

                    product_variation_list = []
                    cart_item_ids = []
                    for item in cart_items:
                        variations = item.variations.all()
                        product_variation_list.append(list(variations))
                        cart_item_ids.append(item.id)

                    user_cart_items = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    user_cart_item_ids = []
                    for item in user_cart_items:
                        existing_variations = item.variations.all()
                        ex_var_list.append(list(existing_variations))
                        user_cart_item_ids.append(item.id)

                    for i, pr in enumerate(product_variation_list):
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = user_cart_item_ids[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += cart_items[i].quantity
                            item.save()
                            cart_items[i].delete()
                        else:
                            cart_item = CartItem.objects.get(id=cart_item_ids[i])
                            cart_item.user = user
                            cart_item.cart = None
                            cart_item.save()

                    # Delete the session cart after merging
                    cart.delete()

            except Cart.DoesNotExist:
                pass

            auth.login(request, user)
            messages.success(request, "Login successful.")
            url = request.META.get('HTTP_REFERER')  # Get the URL of the page that made the request
            try:
                query = requests.utils.urlparse(url).query  # Parse the URL to get the query parameters
                params = dict(x.split('=') for x in query.split('&'))  # Convert query parameters to a dictionary
                if 'next' in params:  # Check if 'next' parameter exists
                    return redirect(params['next'])  # Redirect to the next page
            except:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'accounts/login.html') 

@login_required(login_url='login')  
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link.")
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userProfile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userProfile': userProfile,
    }
    return render(request, 'accounts/dashboard.html', context)

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if account.objects.filter(email=email).exists():
            user = account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password.'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset email has been sent to your email address.")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist.")
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password.")
        return redirect('resetpassword')
    else:
        messages.error(request, "This link has expired.")
        return redirect('login')
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = account._default_manager.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('resetpassword')
    return render(request, 'accounts/resetpassword.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()
    context = {
        'orders': orders,
        'orders_count': orders_count,
    }
    return render(request, 'accounts/my_orders.html', context)
    

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileform(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')
        else:
            # If the forms are invalid, render the form with the submitted data and errors
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request, 'accounts/edit_profile.html', context)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileform(instance=userprofile)
    context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }
    return render(request, 'accounts/edit_profile.html', context)

from django.contrib.auth import update_session_auth_hash


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return render(request, 'accounts/change_password.html')

        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'accounts/change_password.html')

        if new_password and new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, "Password changed successfully.")
            return redirect('change_password')
        else:
            messages.error(request, "Please enter a valid new password.")
            return render(request, 'accounts/change_password.html')
    else:
        return render(request, 'accounts/change_password.html')

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for item in order_detail:
        subtotal += item.product_price * item.quantity
    grand_total = subtotal + order.tax
    context = {

        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'grand_total': grand_total,
    }
    return render(request, 'accounts/order_detail.html', context)
