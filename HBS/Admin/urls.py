from django.urls import path
from Admin import views

urlpatterns =[
        path('Admin/Profile',views.A_profile,name='A-profile'),

        path('Add/Department',views.add_department,name='add-department'),
        path('Add/Department/Data',views.add_department_data,name='add-department-data'),
        path('View/Department',views.view_department,name='view-department'),
        path('Edit/Department/<int:pk>',views.edit_department,name='edit-department'),
        path('Edit/Department/Data/<int:pk>',views.edit_department_data,name='edit-department-data'),
        path('Delete/Department/<int:pk>',views.delete_department,name='delete-department'),

        path('Messages/',views.notification, name='messages'),
        path('Querys/',views.querys,name='querys_page'),

        path('Patient/Requests/',views.patient_requests,name='patient-requests'),
        path('Approve/Patient/Request/<int:pk>',views.approve_patient_request,name='approve-patient-request'),
        path('Reject/Patient/Request/<int:pk>',views.reject_patient_request,name='reject-patient-request'),
        path('patinet/request/replay/<int:pk>',views.patient_request_replay,name='patient-request-replay'),

        path('Doctor/Requests/',views.doctor_requests,name='doctor-requests'),
        path('Approve/Requests/<int:pk>',views.approve_request,name='approve-requests'),
        path('Reject/Requests/<int:pk>',views.request_reject,name='request-reject'),
        path('Reject/Doctor/Request/Replay/<int:pk>',views.request_replay,name='request-replay'),

        path('Replay/<int:pk>/',views.query_replay,name='replay'),
        path('Send-Replay/<int:pk>',views.send_replay,name='send-replay'),

        path('Add/Patient',views.add_patient,name='add-patient'),
        path('Add/Patient/Data',views.add_patient_data,name='add-patient-register-data'),
        path('View/Patient',views.view_patient,name='view-patient'),
        path('Delete/Pateint/<int:pk>',views.delete_patient,name='delete-patient'),

        path('Add/Doctor',views.add_doctor,name='add-doctor'),
        path('Add/Doctor/Data',views.add_doctor_data,name='add-doctor-data'),
        path('View/Doctor',views.view_doctor,name='view-doctor'),
        path('Delete/Doctor/<int:pk>',views.delete_doctor,name='delete-doctor'),

        path('View/Appointments/',views.view_appointments,name='view-appointments'),
        path('Approve/Appointments/<int:pk>',views.approve_appointment,name='approve-appointment'),
        path('Rejection/Appointment/<int:pk>',views.reject_appointment,name='reject-appointment'),
        path('Rejection/Appointment/Data/<int:pk>',views.reject_appointment_data,name='reject-appointment-data'),

        path('Consultation/Status/',views.Consultation_status,name='consultation-status'),
        path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),

]