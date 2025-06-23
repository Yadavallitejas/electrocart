from . import views
from django.urls import path


urlpatterns = [
    path('', views.cart, name='cart'),  # Cart view
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),  # Add to cart view
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),  # Remove from cart view
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),  # Remove cart item view
    path('checkout/', views.checkout, name='checkout'),  # Checkout view

]