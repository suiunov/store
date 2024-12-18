from django.urls import path
from store.views import ProductAPIListView, ProductAPIDetailView, CartAPIView, home

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductAPIListView.as_view(), name='product_list'),
    path('products/<int:product_id>/', ProductAPIDetailView.as_view(), name='product_detail'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/<int:product_id>/', CartAPIView.as_view(), name='cart_detail'),
]
