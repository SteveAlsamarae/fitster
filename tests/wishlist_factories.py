import factory
from store.wishlist.models import Wishlist, WishlistItem

from .customer_factories import CustomerFactory
from .products_factories import ProductFactory


class WishlistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wishlist

    user = factory.SubFactory(CustomerFactory)


class WishlistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistItem

    wishlist = factory.SubFactory(WishlistFactory)
    product = factory.SubFactory(ProductFactory)