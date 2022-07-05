from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet

import json
import requests

from .models import NewsleterAccount
from django.conf import settings


api_url: str = f'https://{settings.MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint: str = f'{api_url}/lists/{settings.MAILCHIMP_EMAIL_LIST_ID}/members'


def subscribe_email(email: str) -> tuple:
    """Subscribe email to mailchimp mail-list

    Args:
        email (str): Customer email address

    Returns:
        (tuple): Response status code and response body as json
    """

    data: dict = {
        "email_address": email,
        "status": "subscribed"
    }
    req = requests.post(
        members_endpoint,
        auth=("", settings.MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return req.status_code, req.json()


def newsleter_email_list(request: HttpRequest) -> HttpResponse:
    """View for newsletter subscription

    Args:
        request (HttpRequest): Django request object

    Returns:
        HttpResponse: Django response object
    """

    if request.method == "POST":
        email: str = request.POST.get('email', None)
        email_query: QuerySet = NewsleterAccount.objects.filter(email=email)

        if email:
            if email_query.exists():
                return render(request, "newsletter/_error.html")
            else:
                try:
                    subscribe_email(email)
                    subscribed = NewsleterAccount.objects.create(email=email)
                    subscribed.save()
                    return render(request, "newsletter/_success.html")
                except Exception as e:
                    print(f"Error - {e}")
                    return render(request, "newsletter/_error.html")
        else:
            return render(request, "newsletter/_error.html")
