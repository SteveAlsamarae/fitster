from django.forms import ModelForm
from django import forms

from .models import ContactMessage


class ConactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "phone",
            "subject",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                    "required": "required",
                    "autofocus": "autofocus",
                    "maxlength": "255",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                    "required": "required",
                    "maxlength": "80",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                    "required": "required",
                    "maxlength": "12",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your subject",
                    "required": "required",
                    "maxlength": "255",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your message",
                    "required": "required",
                    "rows": "8",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ConactForm, self).__init__(*args, **kwargs)

        self.fields[
            "name"
        ].help_text = "Enter your name in the format of 'Firstname Lastname'"
        self.fields["subject"].help_text = "Enter an eye-catching subject"
        self.fields[
            "message"
        ].help_text = "Write your message in detail. Please be as detailed as possible"
