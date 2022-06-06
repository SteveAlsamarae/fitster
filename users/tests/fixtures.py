import pytest
from pytest_factoryboy import register

from tests.users_factories import * # noqa: F403,F401

register(UserProfileFactory)
register(DeliveryAddressFactory)
register(ShippingAddressFactory)

@pytest.fixture
def user_profile(db, user_profile_factory):
    _user_profile = user_profile_factory.create()
    return _user_profile

@pytest.fixture
def delivery_address(db, delivery_address_factory):
    _delivery_address = delivery_address_factory.create()
    return _delivery_address

@pytest.fixture
def shipping_address(db, shipping_address_factory):
    return shipping_address_factory.create()