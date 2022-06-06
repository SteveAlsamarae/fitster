import pytest
from pytest_factoryboy import register

from tests.classes_factories import *  # noqa: F401


register(FitnessClassFactory)
register(TrainerFactory)
register(TrainerSkillFactory)
register(ClassScheduleFactory)
register(FitnessSubscriptionPlanFactory)
register(FitnessSubscriptionFactory)


@pytest.fixture
def fitness_class(db, fitness_class_factory):
    fitness_class = fitness_class_factory.create()
    return fitness_class


@pytest.fixture
def trainer(db, trainer_factory):
    trainer = trainer_factory.create()
    return trainer


@pytest.fixture
def trainer_skills(db, trainer_skill_factory):
    trainer_skills = trainer_skill_factory.create_batch(3)
    return trainer_skills


@pytest.fixture
def class_schedule(db, class_schedule_factory):
    class_schedule = class_schedule_factory.create()
    return class_schedule


@pytest.fixture
def fitness_subscription_plan(db, fitness_subscription_plan_factory):
    fitness_subscription_plan = fitness_subscription_plan_factory.create()
    return fitness_subscription_plan


@pytest.fixture
def fitness_subscription(db, fitness_subscription_factory):
    fitness_subscription = fitness_subscription_factory.create()
    return fitness_subscription
