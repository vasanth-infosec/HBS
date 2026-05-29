from django.db import models
from Home.models import PatientModel,DoctorModel
from patient.models import AppointmentModel

# Create your models here.

class ConsultationModels(models.Model):

    appointment=models.ForeignKey(AppointmentModel,on_delete=models.CASCADE,related_name='consultations')
    doctor=models.ForeignKey(DoctorModel,on_delete=models.CASCADE,null=True)
    patient=models.ForeignKey(PatientModel,on_delete=models.CASCADE,null=True)
    patient_name = models.TextField(null=True)
    doctor_name = models.TextField(null=True)
    diagnosis=models.TextField()
    prescription=models.TextField()
    notes=models.TextField(null=True,blank=True)
    reason = models.CharField(max_length=300 ,default='No Reason',null=True)
    created_at=models.DateTimeField(auto_now_add=True)