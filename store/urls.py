from django.urls import path
from . import views  # Import the views module from the current package
urlpatterns = [
    path('', views.store, name='store'),  # Add this line to include the home view
    path('categor/<slug:category_slug>/', views.store, name='product_by_category'),  # URL pattern for filtering products by category
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # URL pattern for product detail view
    path('search/', views.search, name='search'),  # URL pattern for search functionality
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),  # URL pattern for submitting a review


]