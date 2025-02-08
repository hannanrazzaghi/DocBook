from django.test import TestCase
from booking.models import Admin, Doctor, Patient, Appointment
from django.utils import timezone

class MigrationTestCase(TestCase):

    def setUp(self):
        self.admin = Admin.objects.create(username='admin', password='admin')
        self.doctor = Doctor.objects.create(name='Dr. Smith', specialization='cardiology', schedule=self.schedule)
        self.patient = Patient.objects.create(name='John Doe', email='john@example.com', password='password', medical_history='None')
        self.appointment = Appointment.objects.create(doctor=self.doctor, patient=self.patient, date_time=timezone.now())

    def test_migrations(self):
        self.assertEqual(self.schedule.day, 'Monday')
        self.assertEqual(self.admin.username, 'admin')
        self.assertEqual(self.doctor.name, 'Dr. Smith')
        self.assertEqual(self.patient.email, 'john@example.com')
        self.assertEqual(self.appointment.status, 'Pending')

