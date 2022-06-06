import uuid

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

PHONE_NUMBER_VALIDATOR = RegexValidator(r"^[0-9]{9,11}$", "Phone number is not valid.")
DAY_CHOICES = (
    ("Mon", _("Monday")),
    ("Tue", _("Tuesday")),
    ("Wed", _("Wednesday")),
    ("Thu", _("Thursday")),
    ("Fri", _("Friday")),
    ("Sat", _("Saturday")),
    ("Sun", _("Sunday")),
)


class Trainer(models.Model):
    """Trainer model to store trainer information."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, blank=True, null=True)
    title = models.CharField(max_length=50, verbose_name=_("Trainer title"))
    avatar = models.ImageField(upload_to="avatars", verbose_name=_("avatar"))
    introduction = models.TextField(verbose_name=_("Introduction"))
    personal_summery = models.TextField(verbose_name=_("Personal summery"))
    email = models.EmailField(verbose_name=_("Email"))
    phone_number = models.CharField(
        max_length=11,
        validators=[PHONE_NUMBER_VALIDATOR],
        verbose_name=_("Phone Number"),
    )
    address = models.CharField(max_length=150, verbose_name=_("Address"))
    facebook = models.CharField(max_length=100, verbose_name=_("Facebook Link"), blank=True, null=True)
    twitter = models.CharField(max_length=100, verbose_name=_("Twitter Link"), blank=True, null=True)
    instagram = models.CharField(max_length=100, verbose_name=_("Instagram Link"), blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Trainer.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + "_" + str(counter)
                        counter += 1
                except Trainer.DoesNotExist:
                    self.slug = slug
                    break
        super(Trainer, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("classes:trainer", kwargs={"slug": self.slug})

    def get_trainer_skills(self) -> list[object]:
        """Get trainer's skills."""

        return self.skills.all()


class TrainerSkill(models.Model):
    """Trainer skill model for trainer model."""

    trainer = models.ForeignKey(
        Trainer,
        related_name="skills",
        on_delete=models.CASCADE,
    )
    skill = models.CharField(max_length=80, verbose_name=_("Skill"))
    efficiency = models.IntegerField(verbose_name=_("Efficiency"))

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name = _("Trainer Skill")
        verbose_name_plural = _("Trainer Skills")


class FitnessClass(models.Model):
    """Model for FitnessClass to store class data in database"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160, verbose_name=_("Fitness class name"))
    slug = models.SlugField(
        unique=True,
        verbose_name=_("Slug"),
        blank=True,
        null=True,
    )
    thumbnail = models.ImageField(
        upload_to="fitness_class_thumbnails", verbose_name=_("Thumbnail")
    )
    description = models.TextField(verbose_name=_("Class description"))
    phone = models.CharField(
        max_length=20, verbose_name=_("Phone"), validators=[PHONE_NUMBER_VALIDATOR]
    )
    email = models.EmailField(verbose_name=_("Email"))
    address = models.CharField(max_length=160, verbose_name=_("Address"))
    attachment = models.FileField(
        upload_to="fitness_class_attachments", verbose_name=_("Attachment")
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = FitnessClass.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + "_" + str(counter)
                        counter += 1
                except FitnessClass.DoesNotExist:
                    self.slug = slug
                    break
        super(FitnessClass, self).save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("classes:details", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Fitness class")
        verbose_name_plural = _("Fitness classes")

    def get_class_schedules(self) -> list[object]:
        return self.class_schedules.all()

    def get_all_trainers(self) -> list[object]:
        """Get all trainers in class."""

        trainers = [class_sch.trainer for class_sch in self.class_schedules.all()]

        return set(trainers)


class ClassSchedule(models.Model):
    """Model for ClassSchedule to store class schedule data in database"""

    fitness_class = models.ForeignKey(
        FitnessClass,
        verbose_name=_("Fitness class"),
        related_name="class_schedules",
        on_delete=models.CASCADE,
    )
    trainer = models.ForeignKey(
        Trainer,
        verbose_name=_("Trainer"),
        related_name="trainer",
        on_delete=models.CASCADE,
    )
    day = models.CharField(max_length=10, verbose_name=_("Day"), choices=DAY_CHOICES)
    start_time = models.TimeField(verbose_name=_("Start time"))
    end_time = models.TimeField(verbose_name=_("End time"))

    def __str__(self):
        return self.day

    class Meta:
        verbose_name = _("Class schedule")
        verbose_name_plural = _("Class schedules")


class FitnessSubscriptionPlan(models.Model):
    """Model for FitnessSubscriptionPlan to store subscription plan data in database"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name=_("Plan name"))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )
    description = models.TextField(verbose_name=_("Description"))
    stripe_price_id = models.CharField(verbose_name=_("Stripe price id"), max_length=50)
    thumbnail = models.ImageField(
        upload_to="fitness_plan_thumbnail", verbose_name=_("Thumbnail")
    )

    def __str__(self) -> str:
        return self.name

    def get_lines_from_description(self) -> list[str]:
        """Get lines from description."""
        if self.description:
            lines: list[str] = [
                line.strip("-").strip() for line in self.description.split("\n") if line
            ]
        else:
            lines: list = []

        return lines

    class Meta:
        verbose_name = _("Fitness subscription plan")
        verbose_name_plural = _("Fitness subscription plans")


class FintnessSubscription(models.Model):
    """Model for FitnessSubscription to store subscription data in database"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fitness_plan = models.ForeignKey(
        FitnessSubscriptionPlan,
        verbose_name=_("Fitness Plan"),
        on_delete=models.CASCADE,
        related_name="fitness_subscriptions",
    )
    customer = models.ForeignKey(
        User,
        verbose_name=_("Customer"),
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    stripe_sub_key = models.CharField(
        max_length=150, verbose_name=_("Stripe subscription key")
    )
    stripe_session_key = models.CharField(
        max_length=150, verbose_name=_("Stripe session key")
    )
    is_active = models.BooleanField(default=False, verbose_name=_("Is active"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.fitness_plan.name

    class Meta:
        verbose_name = _("Fitness subscription")
        verbose_name_plural = _("Fitness subscriptions")


class NutritionPlan(FitnessSubscriptionPlan):
    """Model for NutritionPlan to store nutrition plan data in database"""

    class Meta:
        verbose_name = _("Nutrition plan")
        verbose_name_plural = _("Nutrition plans")


class NutritionSubscription(FintnessSubscription):
    """Model for NutritionSubscription to store nutrition subscription data in database"""

    class Meta:
        verbose_name = _("Nutrition subscription")
        verbose_name_plural = _("Nutrition subscriptions")
