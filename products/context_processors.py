from .models import Category


def categories_processor(request):
    """
    Expose product categories globally for site-wide navigation and footer links.
    """
    try:
        return {
            "footer_categories": Category.objects.all()
        }
    except Exception:
        return {
            "footer_categories": []
        }
