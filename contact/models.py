from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
