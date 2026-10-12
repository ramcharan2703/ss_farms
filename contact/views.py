
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
            # Save the inquiry first so email failures never lose the lead.
            inquiry = form.save()
            email_sent = False

            try:
                recipient = getattr(
                    settings,
                    "CONTACT_NOTIFICATION_EMAIL",
                    "ssfarmswanaparthy@gmail.com",
                )

                subject = f"New Contact Message from {inquiry.name}"

                body = (
                    "New Inquiry Received\n\n"
                    f"Date: {timezone.now().strftime('%d-%m-%Y %I:%M %p')}\n"
                    f"Name: {inquiry.name}\n"
                    f"Email: {inquiry.email}\n"
                    f"Phone: {inquiry.phone}\n\n"
                    f"Message:\n{inquiry.message}\n"
                )

                sent_count = send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )

                email_sent = sent_count == 1

                if not email_sent:
                    logger.error(
                        "Email notification was not accepted for inquiry #%s.",
                        inquiry.id,
                    )

            except Exception:
                logger.exception(
                    "Contact email dispatch failed for inquiry #%s.",
                    inquiry.id,
                )

            if email_sent:
                messages.success(
                    request,
                    "Your inquiry has been received successfully. "
                    "We will contact you soon.",
                )
            else:
                messages.success(
                    request,
                    "Your inquiry has been received successfully. "
                    "We will contact you soon.",
                )

            return redirect("contact")

        messages.error(
            request,
            "Please correct the errors in the contact form below.",
        )

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
