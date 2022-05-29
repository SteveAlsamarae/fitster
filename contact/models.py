import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    """Contact message model to store contact messages"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, verbose_name=_("Name"))
    email = models.EmailField(max_length=60, verbose_name=_("Email"))
    phone = models.CharField(
        max_length=12, verbose_name=_("Phone"), blank=True, null=True
    )
    subject = models.CharField(max_length=60, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")

    def __str__(self):
        return f"{self.name} - {self.email}"
