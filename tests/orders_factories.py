import factory

from .customer_factories import CustomerFactory
from .products_factories import ProductFactory
from store.orders.models import Order, OrderItem


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(CustomerFactory)
    order_status = 0
    stripe_session_id = 'test_session_id'
    is_active = True


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
