from django.contrib import admin
from .models import Order, OrderedItem, CustomUser, FoodItem
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(CustomUser)
admin.site.register(FoodItem)