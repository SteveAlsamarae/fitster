import pytest
from pytest_factoryboy import register

from tests.contact_factories import ContactMessageFactory


register(ContactMessageFactory)
register(
    ContactMessageFactory,
    "contact_message_by_john",
    name="John Doe",
    email="john@mail.com",
    phone="+1-555-555-5555",
    subject="Test subject",
    message="Test Message",
)


@pytest.fixture
def contact_message(db, contact_message_factory):
    contact_us = contact_message_factory.create()
    return contact_us


@pytest.fixture
def contact_by_john(db, contact_message_by_john):
    contact_us = contact_message_by_john
    return contact_us
