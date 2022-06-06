import datetime
from django.urls import reverse
from django.db.models import QuerySet

from tests.classes_factories import *  # noqa: F401
from classes.tests.fixtures import *  # noqa: F401


def test_fitness_class_factory(fitness_class_factory):
    assert fitness_class_factory is not None
    assert fitness_class_factory is FitnessClassFactory


def test_fitness_class_model(fitness_class):
    assert fitness_class is not None
    assert isinstance(fitness_class, FitnessClass)


def test_fitness_class_model_params(fitness_class):
    assert fitness_class.name == "Fitness Class"
    assert fitness_class.slug == "fitness-class"
    assert fitness_class.description == "Fitness Class Description"
    assert fitness_class.phone == "01234567891"
    assert fitness_class.email == "fitness@mail.com"
    assert fitness_class.address == "Fitness Class Address"
    assert fitness_class.attachment is not None


def test_fitness_class_str(fitness_class):
    assert str(fitness_class) == fitness_class.name


def test_fitness_class_absolute_url(fitness_class):
    class_url = reverse("classes:details", kwargs={"slug": fitness_class.slug})
    assert fitness_class.get_absolute_url() == class_url


def test_fitness_class_meta_verbose_name(fitness_class):
    assert FitnessClass._meta.verbose_name == "Fitness class"
    assert FitnessClass._meta.verbose_name_plural == "Fitness classes"


def test_get_class_schedules(fitness_class):
    assert fitness_class.get_class_schedules().exists() is False


def test_get_class_schedules_type(fitness_class):
    assert isinstance(fitness_class.get_class_schedules(), QuerySet)


def test_trainer_factory(trainer_factory):
    assert trainer_factory is not None
    assert trainer_factory is TrainerFactory


def test_trainer_model(trainer):
    assert trainer is not None
    assert isinstance(trainer, Trainer)


def test_trainer_model_params(trainer):
    assert trainer.name == "Trainer"
    assert trainer.slug == "trainer"
    assert trainer.title == "Trainer Title"
    assert trainer.introduction == "Trainer Introduction"
    assert trainer.personal_summery == "Trainer Personal Summary"
    assert trainer.phone_number == "01234567891"
    assert trainer.email == "trainer@mail.com"
    assert trainer.address == "Trainer Address"
    assert trainer.avatar is not None


def test_trainer_str(trainer):
    assert str(trainer) == trainer.name


def test_trainer_absolute_url(trainer):
    trainer_url = reverse("classes:trainer", kwargs={"slug": trainer.slug})
    assert trainer.get_absolute_url() == trainer_url


def test_get_trainer_skills(trainer):
    assert trainer.get_trainer_skills().exists() is False


def test_get_trainer_skills_type(trainer):
    assert isinstance(trainer.get_trainer_skills(), QuerySet)


def test_trainer_skill_factory(trainer_skill_factory):
    assert trainer_skill_factory is not None
    assert trainer_skill_factory is TrainerSkillFactory


def test_trainer_skill_model(trainer_skill):
    assert trainer_skill is not None
    assert isinstance(trainer_skill, TrainerSkill)


def test_trainer_skill_model_params(trainer_skill):
    assert trainer_skill.trainer is not None


def test_trainer_of_skills(trainer_skill, trainer):
    assert trainer_skill.trainer.name == trainer.name


def test_trainer_skills_meta_verbose_name(trainer_skill):
    assert TrainerSkill._meta.verbose_name == "Trainer Skill"
    assert TrainerSkill._meta.verbose_name_plural == "Trainer Skills"


def test_trainer_skill_str(trainer_skill):
    assert str(trainer_skill) == trainer_skill.skill


def test_trainer_skill_params(trainer_skill):
    assert trainer_skill.skill == "Trainer Skill"
    assert trainer_skill.efficiency == 90


def test_class_schedule_factory(class_schedule_factory):
    assert class_schedule_factory is not None
    assert class_schedule_factory is ClassScheduleFactory


def test_class_schedule_model(class_schedule):
    assert class_schedule is not None
    assert isinstance(class_schedule, ClassSchedule)


def test_class_schedule_model_params(class_schedule):
    assert class_schedule.fitness_class is not None
    assert class_schedule.trainer is not None
    assert class_schedule.start_time == datetime.time(hour=10, minute=0)
    assert class_schedule.end_time == datetime.time(hour=12, minute=0)
    assert class_schedule.day == "Mon"


def test_class_schedule_str(class_schedule):
    assert str(class_schedule) == class_schedule.day


def test_class_schedule_verbose_name(class_schedule):
    assert ClassSchedule._meta.verbose_name == "Class schedule"
    assert ClassSchedule._meta.verbose_name_plural == "Class schedules"


def test_fitness_subscription_plan_factory(fitness_subscription_plan_factory):
    assert fitness_subscription_plan_factory is not None
    assert fitness_subscription_plan_factory is FitnessSubscriptionPlanFactory


def test_fitness_subscription_plan_model(fitness_subscription_plan):
    assert fitness_subscription_plan is not None
    assert isinstance(fitness_subscription_plan, FitnessSubscriptionPlan)


def test_fitness_subscription_plan_model_params(fitness_subscription_plan):
    assert fitness_subscription_plan.name == "Fitness Subscription Plan"
    assert (
        fitness_subscription_plan.description == "Fitness Subscription Plan Description"
    )
    assert fitness_subscription_plan.price == 99
    assert fitness_subscription_plan.stripe_price_id == "price_123456"
    assert fitness_subscription_plan.thumbnail is not None


def test_fitness_subscription_plan_str(fitness_subscription_plan):
    assert str(fitness_subscription_plan) == fitness_subscription_plan.name


def test_get_lines_from_desc_exists(fitness_subscription_plan):
    assert fitness_subscription_plan.get_lines_from_description() is not None


def test_fitness_subscription_factory(fitness_subscription_factory):
    assert fitness_subscription_factory is not None
    assert fitness_subscription_factory is FitnessSubscriptionFactory


def test_fitness_subscription_model(fitness_subscription):
    assert fitness_subscription is not None
    assert isinstance(fitness_subscription, FintnessSubscription)


def test_fitness_subscription_model_params(fitness_subscription):
    assert fitness_subscription.customer is not None
    assert fitness_subscription.fitness_plan is not None
    assert fitness_subscription.is_active is True
    assert fitness_subscription.stripe_sub_key == "subscription_123456"
    assert fitness_subscription.stripe_session_key == "session_123456"


def test_fitness_subscription_str(fitness_subscription):
    assert str(fitness_subscription) == fitness_subscription.fitness_plan.name


def test_fitness_subscription_verbose_name(fitness_subscription):
    assert FintnessSubscription._meta.verbose_name == "Fitness subscription"
    assert FintnessSubscription._meta.verbose_name_plural == "Fitness subscriptions"
