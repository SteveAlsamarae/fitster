from django.db import models
from django.utils.translation import ugettext_lazy as _


class NewsleterAccount(models.Model):
    """Newsletter model to subscribe users to newsletter"""

    email = models.EmailField(verbose_name=_('Email'))
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    def __str__(self):
        return f"User<{self.email}>"
