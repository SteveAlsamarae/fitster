from django.urls import reverse
from django.db.models import QuerySet
from django.contrib.auth.models import User

from users.models import UserProfile, DeliveryAddress, ShippingAddress

from tests.users_factories import * # noqa: F403,F401
from users.tests.fixtures import * # noqa: F403,F401


def test_user_profile_factory(user_profile_factory):
    assert user_profile_factory is not None
    assert user_profile_factory is UserProfileFactory

def test_user_profile_model(customer_user):
    assert customer_user.profile is not None
    assert isinstance(customer_user.profile, UserProfile)
    assert isinstance(customer_user.profile.user, User)
    assert customer_user.profile.user == customer_user
    assert customer_user.profile.avatar is not None

def test_user_profile_str(customer_user):
    assert str(customer_user.profile) == f"{customer_user.username}'s profile"

def test_user_profile_has_delete_method(customer_user):
    assert hasattr(customer_user.profile, 'delete')

def test_delervery_address_factory(delivery_address_factory):
    assert delivery_address_factory is not None
    assert delivery_address_factory is DeliveryAddressFactory

def test_delivery_address_model(delivery_address):
    assert delivery_address.customer is not None
    assert delivery_address.name is not None
    assert delivery_address.phone is not None
    assert delivery_address.city is not None
    assert delivery_address.postcode is not None
    assert delivery_address.address is not None
    assert delivery_address.area is not None

def test_delivery_address_model_name(delivery_address):
    assert DeliveryAddress._meta.model_name == 'deliveryaddress'
    assert isinstance(delivery_address, DeliveryAddress)

def test_delivery_address_str(delivery_address):
    assert str(delivery_address) == f"{delivery_address.name}'s billing address."

def test_delivery_address_verbose_name(delivery_address):
    assert DeliveryAddress._meta.verbose_name == 'Billing Address (Default)'
    assert DeliveryAddress._meta.verbose_name_plural == 'Billing Addresses (Default)'

def test_delivery_address_params(delivery_address):
    assert delivery_address.name == "John Doe"
    assert delivery_address.phone == "1234567890"
    assert delivery_address.city == "New York"
    assert delivery_address.postcode == "10001"
    assert delivery_address.address == "123 Main St"
    assert delivery_address.area == "New York"

def test_shipping_address_factory(shipping_address_factory):
    assert shipping_address_factory is not None
    assert shipping_address_factory is ShippingAddressFactory

def test_shipping_address_model(shipping_address):
    assert shipping_address.customer is not None
    assert shipping_address.name is not None
    assert shipping_address.phone is not None
    assert shipping_address.city is not None
    assert shipping_address.postcode is not None
    assert shipping_address.address is not None
    assert shipping_address.area is not None

def test_shipping_address_is_default(shipping_address):
    assert shipping_address.is_default is False

def test_is_shipping_address(shipping_address):
    assert shipping_address.is_shipping_address is True

def test_shipping_address_area(shipping_address):
    assert shipping_address.area == "New York"
    assert shipping_address.city == "New York"
    assert shipping_address.postcode == "10001"

def test_shipping_address_str(shipping_address):
    assert str(shipping_address) == f"{shipping_address.name}'s shipping address."

def test_shipping_address_verbose_name(shipping_address):
    assert ShippingAddress._meta.verbose_name == 'Shipping Address'
    assert ShippingAddress._meta.verbose_name_plural == 'Shipping Addresses'

def test_shipping_address_model_name(shipping_address):
    assert ShippingAddress._meta.model_name == 'shippingaddress'
    assert isinstance(shipping_address, ShippingAddress)