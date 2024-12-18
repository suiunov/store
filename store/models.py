from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

    def is_available(self):
        return self.stock > 0

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.quantity > self.product.stock:
            raise ValidationError(f"Cannot add {self.quantity} items. Only {self.product.stock} available.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
