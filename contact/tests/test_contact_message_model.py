from contact.models import ContactMessage
from tests.contact_factories import ContactMessageFactory

from contact.tests.fixtures import *  # noqa: F401


def test_contact_message_factory(contact_message_factory):
    assert contact_message_factory is not None
    assert contact_message_factory is ContactMessageFactory


def test_contact_message_model(contact_message):
    assert contact_message is not None
    assert isinstance(contact_message, ContactMessage)


def test_contact_message_mode_verbose_name(contact_message):
    assert contact_message._meta.verbose_name == "Contact Message"
    assert contact_message._meta.verbose_name_plural == "Contact Messages"


def test_contact_message_name_max_length(contact_message):
    assert contact_message._meta.get_field("name").max_length == 60


def test_contact_message_name_is_not_blank(contact_message):
    assert contact_message._meta.get_field("name").blank is False


def test_contact_message_email_max_length(contact_message):
    assert contact_message._meta.get_field("email").max_length == 60


def test_contact_message_email_is_not_blank(contact_message):
    assert contact_message._meta.get_field("email").blank is False


def test_contact_message_subject_max_length(contact_message):
    assert contact_message._meta.get_field("subject").max_length == 120


def test_contact_message_subject_is_not_blank(contact_message):
    assert contact_message._meta.get_field("subject").blank is False


def test_contact_message_is_not_blank(contact_message):
    assert contact_message._meta.get_field("message").blank is False


def test_contact_message_str_is_not_blank(contact_message):
    assert contact_message.__str__() is not None


def test_contact_message_str(contact_message):
    name = contact_message.name
    email = contact_message.email
    assert contact_message.__str__() == f"{name} - {email}"


def test_contact_message_parametrize(contact_by_john):
    assert contact_by_john is not None
    assert contact_by_john.name == "John Doe"
    assert contact_by_john.email == "john@mail.com"
    assert contact_by_john.phone == "+1-555-555-5555"
    assert contact_by_john.subject == "Test subject"
    assert contact_by_john.message == "Test Message"
