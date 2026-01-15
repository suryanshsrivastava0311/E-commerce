from django.contrib import admin
from .models import Cart,CartItems
admin.site.register(CartItems)
admin.site.register(Cart)

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
class CartItemsAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active')

# Register your models here.
