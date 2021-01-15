from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class NewUser(AbstractUser):
    phone = models.CharField(max_length=100)

    REQUIRED_FIELDS = ['email', 'phone']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'