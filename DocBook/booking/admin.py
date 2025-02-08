from django.contrib import admin
from .models import Admin, Doctor, Patient, Appointment, Slot, Rating

admin.site.register(Admin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Slot)
admin.site.register(Rating)