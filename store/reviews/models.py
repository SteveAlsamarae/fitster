import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from store.products.models import Product


class Review(models.Model):
    """
    Review model to store user's feedback about product in DB.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Product"),
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("User"),
    )
    text = models.TextField(verbose_name=_("Text"))
    rating = models.PositiveSmallIntegerField(verbose_name=_("Rating"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{self.customer} - {self.product}"

    def get_rating_range(self) -> range:
        return range(self.rating)

    def get_blank_rating_range(self) -> range:
        return range(5 - self.rating)
