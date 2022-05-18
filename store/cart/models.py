from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from store.products.models import Product


class Cart(models.Model):
    """User's shopping cart model."""

    user = models.OneToOneField(
        User, related_name="cart", verbose_name=_("Customer"), on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    def get_all_cart_item(self) -> list:
        """Get all products in cart."""

        return self.cart_items.all()

    def get_cart_items_count(self) -> int:
        """Get total quantity of all products in cart."""

        return sum([item.quantity for item in self.cart_items.all()])

    def get_total_quantity(self) -> int:
        """Get total quantity of all products in cart."""

        total_quantity = 0
        for item in self.cart_items.all():
            total_quantity += item.quantity
        return total_quantity

    def get_total_regular_price(self) -> float:
        """Get total regular price of all products in cart."""

        total_price = 0
        for item in self.cart_items.all():
            total_price += item.get_product_regular_price()
        return total_price

    def get_total_discount(self) -> float:
        """Get total discount of all products in cart."""

        total_discount = 0
        for item in self.cart_items.all():
            total_discount += item.get_product_total_discount()
        return total_discount

    def get_final_price(self) -> float:
        """Get final price of all products in cart."""

        total_price = 0
        for item in self.cart_items.all():
            total_price += item.get_product_discount_price()
        return total_price


class CartItem(models.Model):
    """Cart items and quantity for Cart model."""

    cart = models.ForeignKey(
        Cart,
        related_name="cart_items",
        verbose_name=_("Cart"),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(default=0)
    item_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        ordering = ("-item_added",)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_product_regular_price(self) -> float:
        """Return total regular price of a single product."""

        return self.product.regular_price * self.quantity

    def get_product_discount_price(self) -> float:
        """Return total discount price or regular price of a single product"""

        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.regular_price * self.quantity

    def get_product_total_discount(self) -> float:
        """Return total discount of a single product."""

        return abs(self.get_product_regular_price() - self.get_product_discount_price())
