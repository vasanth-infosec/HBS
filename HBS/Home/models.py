from django.db import models
from django.contrib.auth import get_user_model
from Admin.models import Department
 
 

user = get_user_model()

# Create your models here.

class PatientModel(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    admin = models.ForeignKey(user,on_delete=models.SET_NULL,null=True)
    patient_age = models.CharField(max_length=20,null=True)
    patient_id = models.CharField(max_length=20,unique=True,null=True)
    patient_gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    patient_blood_group = models.CharField(max_length=10,choices=BLOOD_GROUP_CHOICES)
    patient_address = models.CharField(max_length=300)
    patient_phone = models.CharField(max_length=12)
    patient_image = models.ImageField(upload_to="patient/") 
    action = models.TextField()
    


class DoctorModel(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    
      
    admin  =  models.ForeignKey(user,on_delete=models.SET_NULL,null=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    
    doctor_age= models.CharField(max_length=20,null=True)
    doctor_gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    
    doctor_address = models.CharField(max_length=300)
    doctor_phone = models.CharField(max_length=12)
    doctor_image = models.ImageField(upload_to="doctor/") 
    mrgno = models.CharField(max_length=100)
    qulification = models.CharField(max_length=100)
    YOE = models.IntegerField()
    hospital_name = models.CharField(max_length=100)
    action = models.TextField()

class QueryModel(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject=models.CharField(max_length=100,null=True)
    message = models.CharField(max_length=300)
    action = models.TextField(null=True)

 
 