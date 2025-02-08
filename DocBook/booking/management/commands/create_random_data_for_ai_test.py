import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from booking.models import Doctor, Patient, Appointment, Rating, Slot

# Specializations to choose from
specializations = [
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
    ('allergy_immunology', 'Allergy and Immunology')
]

# Create doctors with specialties
for i in range(10):
    username = f'doctor_{i}'
    user = User.objects.create_user(username=username, password='password')
    specialization = random.choice(specializations)
    doctor = Doctor(user=user, specialization=specialization[1], location=f'City {random.randint(1, 5)}')
    doctor.save()

# Create patients
for i in range(20):
    username = f'patient_{i}'
    user = User.objects.create_user(username=username, password='password')
    patient = Patient(user=user)
    patient.save()

# Create random appointments
doctors = Doctor.objects.all()
patients = Patient.objects.all()

for i in range(30):
    doctor = random.choice(doctors)
    patient = random.choice(patients)
    appointment_time = timezone.now() + timedelta(days=random.randint(1, 30), hours=random.randint(1, 10))
    appointment = Appointment(doctor=doctor, patient=patient, date_time=appointment_time)
    appointment.save()

# Create random ratings
for i in range(50):
    doctor = random.choice(doctors)
    patient = random.choice(patients)
    rating_score = random.randint(1, 5)
    rating = Rating(doctor=doctor, patient=patient, score=rating_score)
    rating.save()

# Create random slots
for i in range(20):
    doctor = random.choice(doctors)
    slot_time = timezone.now() + timedelta(days=random.randint(1, 10), hours=random.randint(1, 5))
    slot = Slot(doctor=doctor, start_time=slot_time, status='available')
    slot.save()

print("Random data created successfully!")
