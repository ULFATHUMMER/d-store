from django.contrib import admin
from .models import CartItem, Cart,ReturnedItem

# Register your models here.

admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(ReturnedItem)



