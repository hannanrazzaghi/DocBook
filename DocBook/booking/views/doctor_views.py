from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import DoctorSerializer
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from ..models import Slot, Doctor, Appointment


@api_view(['GET'])
def doctor_list(request):
    """Returns a list of all doctors."""
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@login_required
def set_unavailability(request):
    """Allows doctors to mark days as unavailable"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        doctor = Doctor.objects.get(user=request.user)
        date_str = data.get("date")

        if not date_str:
            return JsonResponse({"error": "Date is required"}, status=400)

        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Mark all slots of the selected day as unavailable
        Slot.objects.filter(
            doctor=doctor,
            date=selected_date
        ).update(status='unavailable')

        return JsonResponse({"success": "Unavailability set successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def set_slot_duration_specific_day(request):
    """Set custom slot duration for a specific day"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        doctor = Doctor.objects.get(user=request.user)
        date_str = data.get("date")
        duration = int(data.get("duration"))

        if not date_str or not duration:
            return JsonResponse({"error": "Date and duration required"}, status=400)
        if not 5 <= duration <= 60:
            return JsonResponse({"error": "Duration must be between 5 and 60 minutes"}, status=400)

        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Delete existing slots for the specific day
        Slot.objects.filter(doctor=doctor, date=selected_date).delete()

        # Generate new slots with the specified duration
        start_time = datetime.combine(selected_date, doctor.default_start_time)
        end_time = datetime.combine(selected_date, doctor.default_end_time)
        delta = timedelta(minutes=duration)

        while start_time + delta <= end_time:
            Slot.objects.create(
                doctor=doctor,
                date=selected_date,
                start_time=start_time.time(),
                end_time=(start_time + delta).time(),
                status="available"
            )
            start_time += delta

        return JsonResponse({"success": "Slot duration updated"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

import traceback

@login_required
def get_report_data(request):
    """Provides the total number of appointments this week and average daily appointments"""
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Ensure user is authenticated and linked to a doctor
        if not hasattr(request.user, 'doctor'):
            return JsonResponse({"error": "Doctor not found for this user"}, status=404)

        doctor = request.user.doctor  # Use OneToOneField relation instead of querying manually
        today = datetime.today().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        # FIX: Use 'date_time__date' instead of 'date'
        appointments_this_week = Appointment.objects.filter(
            doctor=doctor,
            date_time__date__range=[start_of_week, end_of_week]  # FIXED LINE
        )

        total_appointments = appointments_this_week.count()
        avg_daily_appointments = round(total_appointments / 7, 2) if total_appointments > 0 else 0

        return JsonResponse({
            "total_appointments": total_appointments,
            "avg_daily_appointments": avg_daily_appointments
        })

    except Exception as e:
        print("Error in get_report_data:", traceback.format_exc())  # Print full error
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
