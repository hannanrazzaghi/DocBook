from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
