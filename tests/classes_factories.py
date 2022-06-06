import datetime
import factory
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from classes.models import (
    FitnessClass,
    ClassSchedule,
    Trainer,
    TrainerSkill,
    FitnessSubscriptionPlan,
    FintnessSubscription,
)
from .customer_factories import CustomerFactory


def _image(name="test.jpg", size=(250, 250)):
    img = Image.new("RGB", size)
    content = img.tobytes()

    return SimpleUploadedFile(name, content=content, content_type="image/jpeg")


class FitnessClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FitnessClass

    name = "Fitness Class"
    slug = "fitness-class"
    description = "Fitness Class Description"
    phone = "01234567891"
    email = "fitness@mail.com"
    address = "Fitness Class Address"
    attachment = _image()


class TrainerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trainer

    name = "Trainer"
    slug = "trainer"
    title = "Trainer Title"
    avatar = _image()
    introduction = "Trainer Introduction"
    personal_summery = "Trainer Personal Summary"
    phone_number = "01234567891"
    email = "trainer@mail.com"
    address = "Trainer Address"


class TrainerSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrainerSkill

    trainer = factory.SubFactory(TrainerFactory)
    skill = "Trainer Skill"
    efficiency = 90


class ClassScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClassSchedule

    fitness_class = factory.SubFactory(FitnessClassFactory)
    trainer = factory.SubFactory(TrainerFactory)
    start_time = datetime.time(hour=10, minute=0)
    end_time = datetime.time(hour=12, minute=0)
    day = "Mon"


class FitnessSubscriptionPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FitnessSubscriptionPlan

    name = "Fitness Subscription Plan"
    price = 99
    description = "Fitness Subscription Plan Description"
    stripe_price_id = "price_123456"
    thumbnail = _image()


class FitnessSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FintnessSubscription

    customer = factory.SubFactory(CustomerFactory)
    fitness_plan = factory.SubFactory(FitnessSubscriptionPlanFactory)
    stripe_sub_key = "subscription_123456"
    stripe_session_key = "session_123456"
    is_active = True
