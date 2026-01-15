from django.db import models
from django.conf import settings
from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    
    
    subtotal = models.FloatField()
    tax = models.FloatField()
    total_amount = models.FloatField()

    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number




