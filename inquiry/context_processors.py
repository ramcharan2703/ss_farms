def cart_count(request):
    """Safely calculate total item count in session cart."""
    cart = request.session.get("cart")
    count = 0
    if isinstance(cart, dict):
        for v in cart.values():
            if isinstance(v, int) and v > 0:
                count += v
    return {"cart_count": count}