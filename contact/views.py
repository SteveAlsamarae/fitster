from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import ConactForm


def contact_us_view(request):

    form = ConactForm()

    if request.method == "POST":
        form = ConactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been submitted successfully. We will get back to you soon.",
            )

            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            email_from = form.cleaned_data.get("email")
            subject = "{subject}<{email}>".format(subject=subject, email=email_from)
            recipient_list = [
                settings.EMAIL_HOST_USER,
            ]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, "contact/contact_success.html")

    return render(request, "pages/contact_us.html", {"form": form})


def get_in_touch(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subsect = f"Message from {name}<{email}>"
        message = request.POST.get("message")
        recipient_list = [
            settings.EMAIL_HOST_USER,
        ]

        if name and email and message:
            send_mail(subsect, message, email, recipient_list)
            return render(request, "contact/contact_success.html")

    return request.META.get("HTTP_REFERER")
