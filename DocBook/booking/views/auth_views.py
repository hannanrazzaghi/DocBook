from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models.doctor_models import Doctor
from ..models.patient_models import Patient

def user_registration(request):
    """Handles user registration for doctors and patients."""
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken!')
            return render(request, 'booking/register.html', {'user_type': user_type})

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return render(request, 'booking/register.html', {'user_type': user_type})

        user = User.objects.create_user(username=username, password=password)

        if user_type == 'doctor':
            specialization = request.POST.get('specialization', '').strip()
            if not specialization:
                messages.error(request, 'Specialization is required for doctors!')
                user.delete()
                return render(request, 'booking/register.html', {'user_type': user_type})
            Doctor.objects.create(user=user, specialization=specialization)

        elif user_type == 'patient':
            medical_history = request.POST.get('medical_history', '').strip()
            Patient.objects.create(user=user, medical_history=medical_history)

        messages.success(request, 'Your account has been created successfully!')
        return redirect('login')

    return render(request, 'booking/register.html')


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'booking/login.html')


def logout_view(request):
    """Handles user logout."""
    logout(request)
    return redirect('login')
