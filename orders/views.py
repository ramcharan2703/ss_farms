import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PreOrderForm

logger = logging.getLogger(__name__)


def preorder(request):
    if request.method == "POST":
        form = PreOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            logger.info("New Pre-Order #%s created for %s", order.id, order.customer_name)
            messages.success(
                request,
                f"Thank you, {order.customer_name}! Your pre-order for {order.product.name} has been received."
            )
            return redirect("preorder_success")
        else:
            messages.error(
                request,
                "Please review the errors highlighted below and re-submit your pre-order."
            )
    else:
        form = PreOrderForm()

    return render(request, "preorder.html", {
        "form": form
    })


def preorder_success(request):
    return render(request, "preorder_success.html")