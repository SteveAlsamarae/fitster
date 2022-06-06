import factory

from .customer_factories import CustomerFactory
from users.models import UserProfile, DeliveryAddress, ShippingAddress


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.RelatedFactory(CustomerFactory, "profile")
    avatar = factory.django.ImageField(color="red")
    name = "John Doe"
    phone = "1234567890"
    email = "john@test.com"


class DeliveryAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeliveryAddress

    customer = factory.SubFactory(CustomerFactory)
    name = "John Doe"
    phone = "1234567890"
    city = "New York"
    postcode = "10001"
    address = "123 Main St"
    area = "New York"


class ShippingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    customer = factory.SubFactory(CustomerFactory)
    name = "John Doe"
    phone = "1234567890"
    city = "New York"
    postcode = "10001"
    address = "123 Main St"
    area = "New York"