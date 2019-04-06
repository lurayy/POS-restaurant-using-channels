from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
# from .consumers import StaffConsumer

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    uuid = models.UUIDField(unique = True,default = uuid.uuid4)
    
class FoodItem(models.Model):
    name = models.CharField(max_length = 200)
    price = models.PositiveIntegerField(default = 100)
    is_active = models.BooleanField(default= True)
    code = models.PositiveIntegerField(unique = True,null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATES = (
        ('PAID', "Paid"),
        ('PENDING', "Pending"),
        ('CANCELED', "Canceled")
    )
    state = models.CharField(max_length=8, choices=STATES, default='PENDING')
    timestamp = models.DateTimeField(default=timezone.now)
    table_number = models.PositiveIntegerField(null = True)
 

class OrderedItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity = models.IntegerField()

def send_ordered_item (sender, instance,**kwargs):
    print(instance)
    print("this")

post_save.connect(send_ordered_item, sender=OrderedItem)