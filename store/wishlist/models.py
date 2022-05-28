from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from store.products.models import Product


class Wishlist(models.Model):
    """User's wishlist model."""

    user = models.OneToOneField(
        User,
        related_name="wishlist",
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist"

    def get_all_wishlist_item(self) -> list:
        """Get all products in user's wishlist."""

        return self.wishlist_items.all()

    def get_wishlist_items_count(self) -> int:
        """Get total quantity of all products in wishlist."""

        return self.wishlist_items.count()


class WishlistItem(models.Model):
    """User's wishlist item model."""

    wishlist = models.ForeignKey(
        Wishlist,
        related_name="wishlist_items",
        verbose_name=_("Wishlist"),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Product")
    )
    item_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")
        ordering = ("-item_added",)

    def __str__(self):
        return f"{self.product.title} in {self.wishlist.user.username}'s wishlist"

    def get_product_regular_price(self) -> float:
        """Return total regular price of a single product."""

        return self.product.regular_price

    def get_product_discount_price(self) -> float:
        """Return total discount price or regular price of a single product"""

        if self.product.discount_price:
            return self.product.discount_price
        return self.product.regular_price

    def get_product_total_discount(self) -> float:
        """Return total discount of a single product."""

        return abs(self.get_product_regular_price() - self.get_product_discount_price())
