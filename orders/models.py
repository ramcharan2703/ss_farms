from django.db import models
from products.models import Product


class PreOrder(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="preorders",
    )
    quantity = models.PositiveIntegerField(default=1)
    preferred_date = models.DateField()
    address = models.TextField()
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pre-Order"
        verbose_name_plural = "Pre-Orders"

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} (Qty: {self.quantity})"