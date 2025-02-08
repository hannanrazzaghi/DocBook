from django.urls import path
from . import views
from .views import set_unavailability, set_slot_duration_specific_day, get_report_data

urlpatterns = [
    # Frontend Views
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.user_registration, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('doctor/<int:doctor_id>/', views.doctor_details, name='doctor_details'),

    # API Endpoints
    # Doctor-related endpoints
    path('api/doctors/', views.doctor_list, name='doctor_list'),
    path('api/doctors/search/', views.search_doctors, name='doctor_search'),
    path('api/doctors/<int:doctor_id>/availability/',
         views.get_available_slots, name='get_available_slots'),
    path('api/doctors/<int:doctor_id>/set_unavailability/',
         views.set_unavailability, name='set_unavailability'),
    # Appointment-related endpoints
    path('api/appointments/book/',
         views.book_appointment, name='book_appointment'),
    path('set_unavailability/', set_unavailability, name='set_unavailability'),
    path('set_slot_duration_specific_day/', set_slot_duration_specific_day, name='set_slot_duration_specific_day'),
    path('get_report_data/', get_report_data, name='get_report_data'),
    path('api/get_doctor_recommendation/', views.get_doctor_recommendation, name='get_doctor_recommendation'),

    ]

