from django.shortcuts import render, redirect
from .forms import RegistrationForm

from .models import account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            # user.phone_number = phone_number
            # user.save()
            # You might want to redirect after successful registration
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Registration successful.")
            return redirect('register')

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
            auth.login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'accounts/login.html') 

@login_required(login_url='login')  
def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')

def activate(request):
    return 

