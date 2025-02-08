from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ..models.doctor_models import Doctor
from ..models.appointment_models import Appointment
from ..serializers import DoctorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required
def user_dashboard(request):
    """Displays user dashboard with search and appointments."""
    query = request.GET.get('q', '')
    search_results = Doctor.objects.filter(Q(user__username__icontains=query) | Q(specialization__icontains=query)) if query else []

    user_role = 'unknown'
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('date_time')
        user_role = 'patient'
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('date_time')
        user_role = 'doctor'
    else:
        appointments = []

    return render(request, 'booking/user_dashboard.html', {
        'appointments': appointments,
        'search_results': search_results,
        'user_role': user_role,
    })


@api_view(['GET'])
@login_required
def search_doctors(request):
    query = request.query_params.get('q', '')
    if not query:
        doctors = Doctor.objects.all()
    else:
        doctors = Doctor.objects.filter(
            Q(user__username__icontains=query) | Q(specialization__icontains=query)
        )
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)
