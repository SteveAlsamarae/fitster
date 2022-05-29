from django.contrib import admin

from .models import (
    ClassSchedule,
    FintnessSubscription,
    FitnessClass,
    FitnessSubscriptionPlan,
    NutritionPlan,
    Trainer,
    TrainerSkill,
)


class ClassScheduleInline(admin.TabularInline):
    model = ClassSchedule
    extra = 2


class TrainerSkillInline(admin.TabularInline):
    model = TrainerSkill
    extra = 2


admin.site.register(
    FitnessClass,
    inlines=[ClassScheduleInline],
    list_display=["name", "slug", "phone", "email"],
    search_fields=["name"],
)

admin.site.register(
    Trainer,
    inlines=[TrainerSkillInline],
    list_display=["name", "title"],
    search_fields=["name"],
)

admin.site.register(FitnessSubscriptionPlan)
admin.site.register(NutritionPlan)
admin.site.register(FintnessSubscription)
