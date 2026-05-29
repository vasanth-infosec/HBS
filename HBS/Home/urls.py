from django.urls import path
from Home import views

urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/',views.login,name='login'),
    path('patient/',views.patient,name='patient'),
    path('doctor/',views.doctor,name='doctor'),
    path('contact/', views.contact, name='contact'),
    path('Query/',views.query,name='query'),

    path('login-data',views.login_data,name='login-data'),
    path('Logout',views.logout,name='logout'),

    path('Patient/Register',views.patient_register,name='patient-reg'),
    path('Doctor/Register',views.doctor_register,name='doctor-reg'),

    
     

]