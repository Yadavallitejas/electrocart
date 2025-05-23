from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.register, name='register'),  # Cart view
    path('login/', views.login, name='login'),  # Add to cart view
    path('logout/', views.logout, name='logout'),  # Remove from cart view
    path('dashboard/', views.dashboard, name='dashboard'),  # Cart view
    path('', views.dashboard, name='dashboard'),  # Add to cart view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Remove from cart view
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),  # Cart view
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),  # Add to cart view
    path('resetpassword/', views.resetpassword, name='resetpassword'),  # Remove from cart view
   
]