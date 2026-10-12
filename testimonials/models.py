from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
    )

    review = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating must be between 1 and 5 stars.",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} ({self.rating}★)"