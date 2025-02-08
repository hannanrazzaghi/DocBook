from django.db import models
from django.utils import timezone
from ..models import Doctor,Patient


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.patient.user.username} with Dr. {self.doctor.user.username} at {self.date_time}"