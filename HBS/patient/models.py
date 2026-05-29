from django.db import models
from django.contrib.auth import get_user_model
from Admin.models import Department
from Home.models import PatientModel,DoctorModel
 
 

user = get_user_model()
# Create your models here.

class AppointmentModel(models.Model):

   
    patient = models.ForeignKey(PatientModel,on_delete=models.SET_NULL,null=True)
    Doctor = models.ForeignKey(DoctorModel,on_delete=models.SET_NULL,null=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    

    appointment_id = models.CharField(max_length=20,unique=True,blank=True,null=True)
    patient_name = models.TextField(null=True)
    doctor_name = models.TextField(null=True)
    appointment_date = models.DateField()
     
    symptoms = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.TextField()
    consultation_status = models.CharField(max_length=200,default='pending',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    patient_age=models.CharField(max_length=20,null=True)
    rejected_reason = models.TextField(blank=True,null=True)
    suggested_date = models.DateField(blank=True,null=True)
    suggested_time = models.TimeField(blank=True,null=True)
    