from rest_framework import serializers
from .models import Doctor, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization']