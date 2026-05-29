from django.urls import path
from doctor import views

urlpatterns = [
    path('Profile',views.doctor_profile,name='D-profile'),
    path('Update/Doctor/Profile',views.update_doctor,name='doctor-update-profile'),
    path('Update/Doctor/Data',views.update_doctor_data,name='update-doctor-data'),
    path('Doctor/Reset/Password',views.update_doctor_password,name='update-doctor-password'),
    path('Doctor/Reset/Password/data',views.update_doctor_password_data,name='update-doctor-password-data'),
    path('View/Toady/Appointments',views.view_today_appointments,name='view-today-appointment'),
    path('Consultation/Form/<int:pk>/', views.consultation_form, name='consultation-form'),
    path('Consultation/Data/<int:pk>',views.consulted,name='consulted'),
    path('Doctor/Upcoming/appointments/',views.view_upcoming_appointments,name='upcoming-appointment'),
    path('Doctor/Appointments/Histroy',views.appointment_histroy,name='doctor-appointment-histroy'),
    path('Patient/Details/',views.patient_details,name='patient-details'),
    path('Patient/Not-Consulatated/<int:pk>',views.not_consulted,name='not-consulted'),
    path('Patient/Not-Consulated/Submit/<int:pk>',views.not_consulted_submit,name='not_consulted_submit'),
    path('Doctor/Dashboard',views.doctor_dashboard,name='doctor-dashboard'),
]