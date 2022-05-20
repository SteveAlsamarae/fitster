import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from store.products.models import Product

ORDER_STATUS = (
    (0, _("Confirmed")),
    (1, _("Processing")),
    (2, _("Delivered")),
    (3, _("Cancelled")),
)


class Order(models.Model):
    """Model for placed orders."""

    user = models.ForeignKey(
        User,
        related_name="orders",
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
    )
    order_id = models.CharField(
        verbose_name=_("Order ID"), editable=False, unique=True, max_length=8
    )
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(choices=ORDER_STATUS, default=0)
    is_active = models.BooleanField(default=True)
    stripe_session_id = models.CharField(
        verbose_name=_("STRIPE SESSION ID"), max_length=100
    )

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = uuid.uuid4().hex[:8].upper()
        return super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-order_time"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{self.user.username}'s order"

    def get_total_price(self):
        total_price = 0
        for item in self.order_items.all():
            total_price += item.get_product_total_price()
        return total_price


class OrderItem(models.Model):
    """Model for items in order."""

    order = models.ForeignKey(
        Order,
        related_name="order_items",
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.DO_NOTHING,
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.product.title} | {self.quantity} units"

    def get_product_total_price(self):
        """Get total price of product."""

        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.regular_price * self.quantity
