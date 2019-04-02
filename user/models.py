from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    uuid = models.UUIDField(unique = True,default = uuid.uuid4)

class manager(CustomUser):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.PositiveIntegerField()
    