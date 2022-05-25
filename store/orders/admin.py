from django.contrib import admin

from store.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


admin.site.register(
    Order,
    readonly_fields=["order_time"],
    inlines=[OrderItemInline],
    list_display=["order_id", "user", "order_time", "order_status"],
)
