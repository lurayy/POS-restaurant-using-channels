from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
# from django.db.models.signals import post_save
# from .consumers import StaffConsumer

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_table = models.BooleanField(default = False)
    uuid = models.UUIDField(unique = True,default = uuid.uuid4)

class Table (models.Model):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = "Table", unique = True)
    table_number = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        self.user.is_manager = False
        self.user.is_staff = False
        self.user.is_table = True
        super().save(*args, **kwargs)

class Supervisor(CustomUser):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = "Supervisor", unique = True)
    contact_number = models.CharField(blank = True, max_length  =  14)

    def save(self, *args, **kwargs):
        self.user.is_manager = True
        self.user.is_staff = True
        self.user.is_table = False
        super().save(*args, **kwargs)


class Staff(CustomUser):
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = "Staff", unique = True)
    contact_number = models.CharField(blank = True, max_length  =  14)

    def save(self, *args, **kwargs):
        self.user.is_manager = False
        self.user.is_staff = True
        self.user.is_table = False
        super().save(*args, **kwargs)

class FoodType(models.Model):
    food_type = models.CharField(max_length = 200,null = True)

    def __str__(self):
        return str(self.food_type)


class FoodItem(models.Model):
    name = models.CharField(max_length = 200)
    food_type = models.ForeignKey(FoodType, on_delete = models.CASCADE,null = True)
    price = models.PositiveIntegerField(default = 100)
    is_active = models.BooleanField(default= True)

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

    def __str__(self):
        return str(self.table_number)
 

class OrderedItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order.table_number) + " ,  " + str(self.food_item)

# def send_ordered_item (sender, instance,**kwargs):
#     print(instance)
#     print("this")

# post_save.connect(send_ordered_item, sender=OrderedItem)
