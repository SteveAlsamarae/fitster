from newsletter.models import NewsleterAccount
from tests.newsletter_factories import NewsletterFactory

from newsletter.tests.fixtures import *  # noqa: F401


def test_newsletter_factory(newsletter_factory):
    assert newsletter_factory is not None
    assert newsletter_factory is NewsletterFactory


def test_newsletter_model(newsletter):
    assert newsletter is not None
    assert isinstance(newsletter, NewsleterAccount)


def test_newsletter_mode_verbose_name(newsletter):
    assert newsletter._meta.verbose_name == "Newsletter"
    assert newsletter._meta.verbose_name_plural == "Newsletters"


def test_newsletter_email_is_not_blank(newsletter):
    assert newsletter._meta.get_field("email").blank is False


def test_newsletter_str_is_not_blank(newsletter):
    assert newsletter.__str__() is not None


def test_newsletter_str(newsletter):
    email = newsletter.email
    assert newsletter.__str__() == f"User<{email}>"
