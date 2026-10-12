import urllib.parse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from products.models import Product

MAX_QUANTITY_PER_ITEM = 50


def _get_cart(request):
    """Retrieve and sanitize session cart dictionary."""
    cart = request.session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
    # Ensure all quantities are positive integers
    sanitized = {}
    for k, v in cart.items():
        if str(k).isdigit() and isinstance(v, int) and 1 <= v <= MAX_QUANTITY_PER_ITEM:
            sanitized[str(k)] = v
    return sanitized


@require_POST
def add_to_cart(request, product_id):
    cart = _get_cart(request)
    product_str_id = str(product_id)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "The requested product does not exist.")
        return redirect("products")

    if product.status == "Out of Stock":
        messages.warning(request, f"{product.name} is currently out of stock.")
        return redirect("product_detail", id=product.id)

    # Optional quantity from POST input, default 1
    try:
        requested_qty = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        requested_qty = 1
    requested_qty = max(1, min(requested_qty, MAX_QUANTITY_PER_ITEM))

    current_qty = cart.get(product_str_id, 0)
    new_qty = min(current_qty + requested_qty, MAX_QUANTITY_PER_ITEM)
    cart[product_str_id] = new_qty
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"Added {product.name} (x{requested_qty}) to your cart.")

    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
        return redirect(referer)
    return redirect("cart")


@require_POST
def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    product_str_id = str(product_id)

    if product_str_id in cart:
        del cart[product_str_id]
        request.session["cart"] = cart
        request.session.modified = True
        messages.info(request, "Item removed from cart.")

    return redirect("cart")


@require_POST
def increase_quantity(request, product_id):
    cart = _get_cart(request)
    product_str_id = str(product_id)

    if product_str_id in cart:
        if cart[product_str_id] < MAX_QUANTITY_PER_ITEM:
            cart[product_str_id] += 1
            request.session["cart"] = cart
            request.session.modified = True
        else:
            messages.warning(
                request,
                f"Maximum quantity limit of {MAX_QUANTITY_PER_ITEM} reached for this item."
            )

    return redirect("cart")


@require_POST
def decrease_quantity(request, product_id):
    cart = _get_cart(request)
    product_str_id = str(product_id)

    if product_str_id in cart:
        cart[product_str_id] -= 1
        if cart[product_str_id] <= 0:
            del cart[product_str_id]
            messages.info(request, "Item removed from cart.")
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")


@require_POST
def clear_cart(request):
    request.session["cart"] = {}
    request.session.modified = True
    messages.info(request, "Your cart has been cleared.")
    return redirect("cart")


def cart(request):
    raw_cart = _get_cart(request)
    product_ids = [int(pid) for pid in raw_cart.keys() if pid.isdigit()]

    # Efficient batch query preventing N+1 queries
    products = Product.objects.filter(id__in=product_ids).select_related("category")
    product_map = {p.id: p for p in products}

    items = []
    total = 0
    active_cart = {}

    for pid_str, quantity in raw_cart.items():
        pid = int(pid_str)
        if pid in product_map:
            product = product_map[pid]
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })
            active_cart[pid_str] = quantity

    # Clean up stale session items if products were removed from DB
    if len(active_cart) != len(raw_cart):
        request.session["cart"] = active_cart
        request.session.modified = True

    # Construct and safely URL-encode WhatsApp inquiry message
    whatsapp_link = ""
    whatsapp_number = getattr(settings, "WHATSAPP_NUMBER", "918790733189")

    if items:
        lines = [
            "Hello SS Farms,",
            "",
            "I would like to order/inquire about the following items from your website:",
            "",
        ]
        for it in items:
            lines.append(f"• {it['product'].name} x {it['quantity']} = ₹{it['subtotal']:.2f}")

        lines.extend([
            "",
            f"Estimated Grand Total: ₹{total:.2f}",
            "",
            "Please confirm availability and dispatch details.",
            "Thank you!",
        ])
        encoded_message = urllib.parse.quote("\n".join(lines))
        whatsapp_link = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

    return render(request, "inquiry/cart.html", {
        "items": items,
        "whatsapp_link": whatsapp_link,
        "total": total,
        "whatsapp_number": whatsapp_number,
    })