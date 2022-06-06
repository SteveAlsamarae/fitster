import factory
from django.contrib.auth.models import User


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_customer"
    email = "tcustomer@mail.com"
    password = "testpassword"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)
