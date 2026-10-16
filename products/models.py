import urllib.parse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from .validators import validate_indian_whatsapp_number, normalize_indian_whatsapp_number


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    STOCK_STATUS = [
        ("In Stock", "In Stock"),
        ("Out of Stock", "Out of Stock"),
        ("Pre Order", "Pre Order"),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    name = models.CharField(max_length=200, db_index=True)

    image = models.ImageField(
        upload_to="products/",
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default="In Stock",
        db_index=True,
    )

    whatsapp_number = models.CharField(
        max_length=20,
        default="918790733189",
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.whatsapp_number:
            normalized = normalize_indian_whatsapp_number(self.whatsapp_number)
            if not normalized:
                raise ValidationError({
                    "whatsapp_number": "Enter a valid 10-digit Indian mobile number (e.g. 8790733189 or 918790733189)."
                })
            self.whatsapp_number = normalized

    def save(self, *args, **kwargs):
        if self.whatsapp_number:
            normalized = normalize_indian_whatsapp_number(self.whatsapp_number)
            if normalized:
                self.whatsapp_number = normalized
        super().save(*args, **kwargs)

    @property
    def normalized_whatsapp_number(self):
        """
        Returns normalized digits-only international format (91XXXXXXXXXX)
        for wa.me links, safely falling back to farm WhatsApp if corrupted.
        """
        normalized = normalize_indian_whatsapp_number(self.whatsapp_number)
        if normalized:
            return normalized
        return getattr(settings, "WHATSAPP_NUMBER", "918790733189")