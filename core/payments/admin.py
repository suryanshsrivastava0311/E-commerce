from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'total_amount',
        'is_paid',
        'stripe_payment_id',
        'created_at',
    )

    list_filter = (
        'is_paid',
        'created_at',
    )

    search_fields = (
        'order_number',
        'stripe_payment_id',
        'user__email',
        'user__username',
    )

    readonly_fields = (
        'order_number',
        'stripe_payment_id',
        'total_amount',
        'created_at',
        'user',
    )

    ordering = ('-created_at',)
