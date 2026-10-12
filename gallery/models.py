from django.db import models


class Gallery(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery/")
    is_active = models.BooleanField(default=True, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return self.title or f"Farm Photo #{self.id}"