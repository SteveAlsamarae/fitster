from django.contrib import admin

from .models import Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
