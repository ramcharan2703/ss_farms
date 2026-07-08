from django.contrib import admin
from .models import PreOrder


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):

    list_display = (
        "customer_name",
        "product",
        "quantity",
        "phone_number",
        "preferred_date",
        "status",
    )

    list_filter = (
        "status",
        "preferred_date",
    )

    search_fields = (
        "customer_name",
        "phone_number",
    )