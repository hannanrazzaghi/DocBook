from datetime import datetime, timedelta, time, date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .patient_models import Patient


class Doctor(models.Model):
    SPECIALIZATIONS = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('general_practice', 'General Practice'),
        ('psychiatry', 'Psychiatry'),
        ('gynecology', 'Gynecology'),
        ('dentistry', 'Dentistry'),
        ('ENT', 'Ear, Nose, and Throat'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('oncology', 'Oncology'),
        ('pulmonology', 'Pulmonology'),
        ('urology', 'Urology'),
        ('rheumatology', 'Rheumatology'),
        ('geriatrics', 'Geriatrics'),
        ('allergy_immunology', 'Allergy and Immunology'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATIONS)
    location = models.CharField(max_length=100, blank=True, null=True)  # Added location (city)
    default_slot_duration = models.PositiveIntegerField(default=15)
    default_start_time = models.TimeField(default=time(10, 0))
    default_end_time = models.TimeField(default=time(19, 0))

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"



class Slot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),  # Add this choice
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"{self.doctor.user.username} - {self.date} - {self.start_time} ({self.status})"


def generate_slots(doctor):
    """Generates 15-minute slots for the next 6 months, skipping Fridays."""
    today = date.today()
    end_date = today + timedelta(days=8)  # Next 6 months

    current_date = today
    while current_date <= end_date:
        if current_date.weekday() == 4:  # Skip Fridays (Friday = 4 in Python datetime)
            current_date += timedelta(days=1)
            continue

        start_time = doctor.default_start_time
        end_time = doctor.default_end_time
        slot_duration = timedelta(minutes=doctor.default_slot_duration)

        current_time = datetime.combine(current_date, start_time)
        end_time_combined = datetime.combine(current_date, end_time)

        while current_time + slot_duration <= end_time_combined:
            Slot.objects.get_or_create(
                doctor=doctor,
                date=current_date,
                start_time=current_time.time(),
                end_time=(current_time + slot_duration).time(),
                defaults={"status": "available"}
            )
            current_time += slot_duration

        current_date += timedelta(days=1)


@receiver(post_save, sender=Doctor)
def create_slots_on_doctor_signup(sender, instance, created, **kwargs):
    """Automatically generate slots when a new Doctor is created."""
    if created:  # Only run when a new doctor is created
        generate_slots(instance)


class Rating(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    score = models.IntegerField()  # Rating score (1 to 5)
    review = models.TextField()

    def __str__(self):
        return f"Rating for Dr. {self.doctor.user.username} by {self.patient.username}"
