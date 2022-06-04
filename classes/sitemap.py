from django.contrib.sitemaps import Sitemap
from .models import FitnessClass, FitnessSubscriptionPlan, Trainer


class FitnessClassSitemap(Sitemap):
    def items(self):
        return FitnessClass.objects.all()


class FitnessPlanSitemap(Sitemap):
    def items(self):
        return FitnessSubscriptionPlan.objects.all()


class TrainerSitemap(Sitemap):
    def items(self):
        return Trainer.objects.all()
