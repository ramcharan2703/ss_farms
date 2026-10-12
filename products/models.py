from django.db import models


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