from django.urls import path
from patient import views

urlpatterns = [
    path('Profile/',views.patient_profile,name='P-profile'),
    path('Update/Profile/',views.update_profile,name='update-profile'),
    path('Update/Patient/Profile/data',views.update_patient_profile_data,name='update-patient-profile-data'),
    path('Reset/Password',views.patient_reset_password,name='patient-password'),
    path('Update/Password/',views.update_patient_password,name='update-patient-password'),

    path('Patient/Booking/Appointment',views.booking_appointment,name='booking-appointment'),
    path('Patient/Booking/Appointment/Data',views.booking_appointment_data,name='booking-appointment-data'),

    path('My Appointments/',views.my_appointment,name='my-appointments'),
    path('Appointment/Histroy',views.appointment_histroy,name='appointment-histroy'),
    

    path('patient/Dashboard',views.patient_dashboard,name='patient-dashboard')
]
