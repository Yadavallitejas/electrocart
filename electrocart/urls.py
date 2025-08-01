"""
URL configuration for electrocart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Import the views module from the current package
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),  # This is the default admin URL
    path('secure_login/', admin.site.urls),
    path('', views.home, name='home'),  # Add this line to include the home view
    path('store/', include('store.urls')),  # Add this line to include the store app URLs
    path('cart/', include('cart.urls')),  # Add this line to include the cart app
    path('accounts/', include('accounts.urls')),  # Add this line to include the accounts app URLs
    path('orders/', include('orders.urls')),  # Add this line to include the orders app URLs

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add this line to serve media files in development