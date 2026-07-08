from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    STOCK_STATUS = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
        ('Pre Order', 'Pre Order'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='products/'
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default='In Stock'
    )

    whatsapp_number = models.CharField(
        max_length=15
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name