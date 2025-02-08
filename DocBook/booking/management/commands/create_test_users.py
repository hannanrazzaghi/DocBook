import random
from django.contrib.auth.models import User
from booking.models import Doctor, Patient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create test users and doctors for testing purposes'

    def handle(self, *args, **kwargs):
        # List of specializations for doctors
        specializations = [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology', 'General Practice', 'Psychiatry'
        ]

        # Create 10 doctors with names Doctor1 to Doctor10
        for i in range(1, 6):
            username = f'd{i}'
            password = 'a'  # Common password for all users
            user = User.objects.create_user(username=username, password=password)

            # Assign a random specialization to the doctor
            specialization = random.choice(specializations)
            doctor = Doctor.objects.create(user=user, specialization=specialization)

            self.stdout.write(self.style.SUCCESS(f'Successfully created doctor: {username}'))

        # Create 20 patients with names Patient1 to Patient20
        for i in range(1, 6):
            username = f'p{i}'
            password = 'a'  # Common password for all users
            user = User.objects.create_user(username=username, password=password)

            # Assign a random medical history to the patient
            medical_history = random.choice(['Diabetes', 'Hypertension', 'Asthma', 'None'])
            patient = Patient.objects.create(user=user, medical_history=medical_history)

            self.stdout.write(self.style.SUCCESS(f'Successfully created patient: {username}'))

        self.stdout.write(self.style.SUCCESS('Test doctors and patients created successfully!'))
