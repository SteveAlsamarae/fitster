import pytest
from pytest_factoryboy import register

from tests.customer_factories import CustomerFactory


register(CustomerFactory)


@pytest.fixture
def customer_user(db, customer_factory):
    new_customer = customer_factory.create()
    return new_customer


@pytest.fixture
def adminuser(db, customer_factory):
    new_customer = customer_factory.create(
        name="admin_user", is_staff=True, is_superuser=True
    )
    return new_customer
