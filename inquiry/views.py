from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product
from urllib.parse import quote
from django.contrib import messages


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart
    messages.success(request, "Product added to cart successfully!")
    return redirect(request.META.get("HTTP_REFERER", "products"))


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")

def cart(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    message = "Hello SS Farms,%0A%0AI'm interested in the following products:%0A%0A"

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

        message += f"• {product.name} × {quantity}%0A"

    message += "%0APlease share the price and availability.%0AThank you."

    whatsapp_link = f"https://wa.me/918790733189?text={message}"

    return render(request, "inquiry/cart.html", {
        "items": items,
        "whatsapp_link": whatsapp_link,
        "total": total,
    })

def increase_quantity(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart

    return redirect("cart")


def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")

def clear_cart(request):
    request.session["cart"] = {}
    return redirect("cart")