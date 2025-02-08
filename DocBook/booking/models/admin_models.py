from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user.username

