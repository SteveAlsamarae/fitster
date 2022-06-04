from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserProfile, DeliveryAddress, ShippingAddress


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


admin.site.site_header = "Fitster"
admin.site.site_title = "Fitster-Site Admin"
admin.site.index_title = "Fitster Admin"

admin.site.register(
    UserProfile,
    UserProfileAdmin,
)
admin.site.register(DeliveryAddress)
admin.site.register(ShippingAddress)
admin.site.unregister(Group)
