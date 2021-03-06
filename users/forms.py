from django import forms
from django.contrib.auth.models import User

from .models import DeliveryAddress, UserProfile, ShippingAddress


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class UserProfileUpdateForm(forms.ModelForm):
    """Fronend form for updating user profile"""

    class Meta:
        model = UserProfile
        fields = ["avatar", "name", "phone"]


class DefaultAddressForm(forms.ModelForm):
    """Customer's default address form"""

    class Meta:
        model = DeliveryAddress
        fields = [
            "name",
            "phone",
            "city",
            "postcode",
            "area",
            "address",
            "is_shipping_address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ShippingAddressForm(forms.ModelForm):
    """Customer's delivery address form"""

    class Meta:
        model = ShippingAddress
        fields = [
            "name",
            "phone",
            "city",
            "postcode",
            "area",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
