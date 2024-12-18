from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls, name='admin'),  # Admin panel

    # Home page route
    path('', views.home, name='home'),  # Displays "Welcome to the Sneaker Store!"

    # API routes
    path('api/products/', views.ProductAPIListView.as_view(), name='product_list'),  # Product list API
    path('api/products/<int:product_id>/', views.ProductAPIDetailView.as_view(), name='product_detail'),  # Product detail API
    path('api/cart/', views.CartAPIView.as_view(), name='cart'),  # Cart API
    path('api/cart/<int:product_id>/', views.CartAPIView.as_view(), name='cart_detail'),  # Cart detail API
]
