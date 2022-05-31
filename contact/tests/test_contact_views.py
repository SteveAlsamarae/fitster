import pytest
from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse

from contact.models import ContactMessage


@pytest.mark.django_db
def test_contact_us_url(client):
    url = reverse("contact_us")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_us_use_correct_template(client):
    url = reverse("contact_us")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "pages/contact_us.html")


@pytest.mark.django_db
def test_contact_us_create_contact_message(client):
    url = reverse("contact_us")
    data = {
        "name": "Test Name",
        "email": "john@mail.com",
        "phone": "123456789",
        "subject": "Test Subject",
        "message": "Test Message",
    }

    response = client.post(url, data)
    assert response.status_code == 200
    assert ContactMessage.objects.count() == 1
    assertTemplateUsed(response, "contact/contact_success.html")
    assert "Your message has been sent successfully." in response.content.decode()


@pytest.mark.django_db
def test_contact_us_view_use_correct_form(client):
    url = reverse("contact_us")
    response = client.get(url)
    assert response.context["form"].__class__.__name__ == "ContactForm"


@pytest.mark.django_db
def test_get_in_touch_post_create_contact_message(client):
    url = reverse("get_in_touch")
    data = {
        "name": "Test Name",
        "email": "test@mail.com",
        "subject": "Test Subject",
        "message": "Test Message",
    }
    respose = client.post(url, data)
    assert respose.status_code == 200
    assertTemplateUsed(respose, "contact/contact_success.html")


@pytest.mark.django_db
def test_get_in_touch_url(client):
    url = reverse("get_in_touch")
    data = {
        "name": "Test Name",
        "email": "test@mail.com",
        "subject": "Test Subject",
        "message": "Test Message",
    }
    http_referer = client.post(url, data)
    assert url == "/contact/trainer/get-in-touch/"
    assert http_referer.get("HTTP_REFERER") is None
    assert http_referer
