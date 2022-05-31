import pytest

from contact.models import ContactMessage
from contact.forms import ContactForm


@pytest.mark.parametrize(
    "name, email, phone, subject, message, expected_is_valid",
    [
        (
            "John Doe",
            "john@mail.com",
            "15555555555",
            "This is a test subject",
            "Test contact message Message",
            True,
        ),
        (
            "Mark",
            "mark@mail.com",
            "",
            "This is a test subject",
            "Test contact message Message",
            True,
        ),
        (
            "",
            "",
            "15555555555",
            "This is a test subject",
            "Test contact message Message",
            False,
        ),
        ("Mark", "mark@mail.com", "", "", "Test contact message Message", False),
        (
            "Mark",
            "mark@mail.com",
            "+1-555-555-5555",
            "Test contact message subject",
            "",
            False,
        ),
    ],
)
def test_contact_form_is_valid(name, email, phone, subject, message, expected_is_valid):
    form = ContactForm(
        data={
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
        }
    )
    assert form.is_valid() == expected_is_valid


def test_create_contact_message(db, client):

    url = "/contact/contact-us/"
    data = {
        "name": "Test User",
        "email": "tuser@mail.com",
        "phone": "15555555555",
        "subject": "Test msg subject",
        "message": "This is a test message",
    }

    response = client.post(url, data)

    assert response.status_code == 200
    assert ContactMessage.objects.count() == 1
    assert ContactMessage.objects.first().name == "Test User"
    assert "Your message has been sent successfully" in response.content.decode()
