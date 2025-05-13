from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.register, name='register'),  # Cart view
    path('login/', views.login, name='login'),  # Add to cart view
    path('logout/', views.logout, name='logout'),  # Remove from cart view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Remove from cart view
   
]