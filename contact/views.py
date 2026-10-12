import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import ContactForm

logger = logging.getLogger(__name__)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # Attempt email dispatch safely; errors are logged, lead is never lost
            try:
                recipient = getattr(settings, "DEFAULT_FROM_EMAIL", "ssfarmswanaparthy@gmail.com")
                subject = f"New Contact Message from {inquiry.name}"
                body = (
                    f"New Inquiry Received\n\n"
                    f"Date: {timezone.now().strftime('%d-%m-%Y %I:%M %p')}\n"
                    f"Name: {inquiry.name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Phone: {inquiry.phone}\n\n"
                    f"Message:\n{inquiry.message}\n"
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(
                    "Contact email dispatch failed for message #%s: %s",
                    inquiry.id,
                    e,
                    exc_info=True,
                )

            messages.success(
                request,
                "Your message has been sent successfully! We will contact you soon."
            )
            return redirect("contact")
        else:
            messages.error(
                request,
                "Please correct the errors in the contact form below."
            )
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})