from django.forms import ModelForm
from django import forms

from markdownx.fields import MarkdownxFormField

from .models import Post


class AddPostForm(ModelForm):

    content = MarkdownxFormField()

    class Meta:
        model = Post
        fields = [
            "thumbnail",
            "title",
            "slug",
            "tags",
            "content",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                    "required": "required",
                    "autofocus": "autofocus",
                    "maxlength": "255",
                }
            ),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)

        self.fields["title"].help_text = "Write a brief title for your post"
        self.fields[
            "slug"
        ].help_text = "Write a human readable unique slug for your post"
        self.fields["content"].help_text = "Post content supports markdown and html"
        self.fields[
            "tags"
        ].help_text = "Tags must be separated by comma, no spacial characters allowed"
