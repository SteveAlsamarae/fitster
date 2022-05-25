from django import forms

from users.models import DeliveryAddress


class AddressForm(forms.ModelForm):
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
        super(AddressForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.label = ""

        self.fields["name"].widget.attrs.update({"placeholder": "Mr. Steve"})
