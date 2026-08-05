from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "rating",
        "is_active",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_active",
    )

    search_fields = (
        "name",
        "review",
    )