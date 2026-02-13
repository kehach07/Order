from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils import timezone
import uuid


class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    user_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=""
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_code = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.address_code:
            self.address_code = f"ADDR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.address_code} - {self.user.email}"
class Order(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    order_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Snapshot of items (map-like structure)
    items_snapshot = models.JSONField(default=dict)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        # net amount calculation
        self.net_amount = (
            self.total_amount + self.tax_amount - self.discount_amount
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )  # snapshot price

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"




