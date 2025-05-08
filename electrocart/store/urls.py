from django.urls import path
from . import views  # Import the views module from the current package
urlpatterns = [
    path('', views.store, name='store'),  # Add this line to include the home view
    path('<slug:category_slug>/', views.store, name='product_by_category'),  # URL pattern for filtering products by category
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # URL pattern for product detail view

]