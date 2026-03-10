from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class PasswordReset(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True ,editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for{self.user.username} at { self.created_when}"


class OrderList(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class Checkout(models.Model):

    PAYMENT_METHODS = [
        ('M-Pesa', 'M-Pesa'),
        ('Card', 'Card'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)

    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

