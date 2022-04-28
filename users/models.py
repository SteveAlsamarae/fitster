from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django_resized import ResizedImageField


PHONE_NUMBER_VALIDATOR = RegexValidator(r"^[0-9]{11}$", "Enter a valid phone number.")
NAME_VALIDATOR = RegexValidator(
    r"^[a-zA-Z ]*$", "Your name should not contain any special character."
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = ResizedImageField(
        size=[300, 300],
        crop=["middle", "center"],
        upload_to="avatars",
        default="default.jpg",
        quality=70,
        keep_meta=False,
        verbose_name="avatar",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100, validators=[NAME_VALIDATOR])
    phone = models.CharField(max_length=11, validators=[PHONE_NUMBER_VALIDATOR])

    def __str__(self):
        return f"{self.user.username}'s profile"

    # delete user's avater when user is deleted
    def delete(self, *args, **kwargs):
        self.avatar.delete()

        return super(UserProfile, self).delete(*args, **kwargs)
