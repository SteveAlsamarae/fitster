from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserProfile, DeliveryAddress


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = [
        "user",
        "name",
        "phone",
        "email",
    ]
    list_filter = ["user"]
    search_fields = ["user"]


admin.site.register(
    UserProfile,
    UserProfileAdmin,
)
admin.site.register(DeliveryAddress)
admin.site.unregister(Group)
