from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Product, Cart
from store.serializers import ProductSerializer

def home(request):
    return HttpResponse("<h1>Welcome to the Sneaker Store!</h1>")

class ProductAPIListView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        try:
            products = Product.objects.all()
            brand = request.query_params.get('brand')
            if brand:
                products = products.filter(brand=brand)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Failed to fetch products", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductAPIDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to fetch product", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CartAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart_items = Cart.objects.filter(user=request.user).select_related('product')
            data = [{
                "id": item.id,
                "product_id": item.product.id,
                "name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "total": item.quantity * item.product.price
            } for item in cart_items]
            return Response(data)
        except Exception as e:
            return Response(
                {"error": "Failed to fetch cart", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if quantity < 1:
                return Response(
                    {"error": "Quantity must be at least 1"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product = Product.objects.get(id=product_id)
            
            if not product.is_available():
                return Response(
                    {"error": "Product is out of stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({
                "message": "Product added to cart",
                "cart_item": {
                    "product": product.name,
                    "quantity": cart_item.quantity
                }
            })
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Failed to add to cart", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, product_id):
        try:
            cart_item = Cart.objects.get(
                user=request.user,
                product_id=product_id
            )
            cart_item.delete()
            return Response({"message": "Product removed from cart"})
        except Cart.DoesNotExist:
            return Response(
                {"error": "Product not found in cart"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Failed to remove from cart", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
