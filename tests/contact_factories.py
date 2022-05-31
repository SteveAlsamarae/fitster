import factory
from faker import Faker

from contact.models import ContactMessage


fake = Faker()


class ContactMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactMessage

    name = factory.LazyAttribute(lambda x: fake.name())
    email = factory.LazyAttribute(lambda x: fake.email())
    phone = factory.LazyAttribute(lambda x: fake.phone_number())
    subject = factory.LazyAttribute(lambda x: fake.sentence(nb_words=6))
    message = factory.LazyAttribute(lambda x: fake.text())
