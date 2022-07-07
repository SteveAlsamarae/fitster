import factory

from newsletter.models import NewsleterAccount


class NewsletterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewsleterAccount

    email = "test@newsleter.com"
