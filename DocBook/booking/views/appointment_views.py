from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from ..models import Doctor, Appointment, Slot, Patient
from django.db import transaction


@permission_classes([IsAuthenticated])
def doctor_details(request, doctor_id):
    """Render the doctor details page."""
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'booking/doctor_details.html', {'doctor': doctor})


@csrf_exempt
def book_appointment(request):
    """Handle appointment booking."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        doctor_id = data.get("doctor_id")
        selected_time = data.get("selected_time")

        # Validate required fields
        if not doctor_id or not selected_time:
            return JsonResponse({"error": "Doctor ID and time are required"}, status=400)

        # Parse and validate datetime
        try:
            appointment_time = timezone.make_aware(datetime.strptime(selected_time, '%Y-%m-%d %H:%M'))
        except ValueError:
            return JsonResponse({"error": "Invalid time format. Use YYYY-MM-DD HH:MM"}, status=400)

        # Prevent past bookings
        if appointment_time <= timezone.now():
            return JsonResponse({"error": "Cannot book appointments in the past"}, status=400)

        # Get doctor and patient
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)

        # Find and lock available slot
        with transaction.atomic():
            slot = get_object_or_404(
                Slot.objects.select_for_update(),
                doctor=doctor,
                date=appointment_time.date(),
                start_time=appointment_time.time(),
                status='available'
            )

            # Create appointment
            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date_time=appointment_time
            )

            # Update slot status
            slot.status = 'reserved'
            slot.save()

        return JsonResponse({
            "success": "Appointment booked successfully",
            "details": {
                "doctor": doctor.user.get_full_name(),
                "time": appointment_time.strftime('%Y-%m-%d %H:%M')
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_slots(request, doctor_id):
    """Return available slots for a doctor on a specific date."""
    date_str = request.GET.get('date')
    if not date_str:
        return Response({"error": "Date parameter is required in YYYY-MM-DD format."}, status=400)

    try:
        target_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": f"Invalid date format: {date_str}. Use YYYY-MM-DD."}, status=400)

    doctor = get_object_or_404(Doctor, pk=doctor_id)
    patient = get_object_or_404(Patient, user=request.user)

    slots = Slot.objects.filter(doctor=doctor, date=target_date).order_by('start_time')
    if not slots.exists():
        return Response({
            "slots": [],
            "message": f"No available slots for {doctor.user.get_full_name()} on {target_date}."
        })

    processed_slots = []
    for slot in slots:
        slot_status = slot.status

        # Check appointments only for available slots
        if slot_status == 'available':
            appointment = Appointment.objects.filter(
                doctor=doctor,
                date_time__date=slot.date,
                date_time__time=slot.start_time
            ).first()

            if appointment:
                slot_status = "reserved" if appointment.patient == patient else "reserved_other"

        processed_slots.append({
            "start_time": slot.start_time.strftime('%H:%M'),
            "end_time": slot.end_time.strftime('%H:%M'),
            "status": slot_status,
        })

    return Response({"slots": processed_slots})