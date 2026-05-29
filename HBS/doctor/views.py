from django.shortcuts import render,redirect
from Home.models import PatientModel,DoctorModel
from django.contrib.auth.models import auth , User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from patient.models import AppointmentModel
from datetime import date
from doctor.models import ConsultationModels
from django.contrib import messages
from Admin.models import Department
import re

# Create your views here.

def doctor_profile(request):
    user = request.user
    data = DoctorModel.objects.get(admin=user)
    patinet = PatientModel.objects.filter(
        appointmentmodel__Doctor=data).distinct().count()
    return render(request,"doctor/doctor-profile.html",{'data':data,
                                                        'patient':patinet})

def update_doctor(request):
    user = request.user
    data= DoctorModel.objects.get(admin=user)
    departments = Department.objects.all() 
    return render(request,'doctor/doctor-update-profile.html',{'data':data,
                                                               'depts':departments})

def update_doctor_data(request):
    user = request.user
    data = DoctorModel.objects.get(admin=user)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        uname = request.POST['username']
        hname = request.POST['hname']
        qual = request.POST['qual']
        dept_id = request.POST['select']
        gender = request.POST['gender']
        old = data.doctor_image
        new = request.FILES.get("file")

        # image update
        if new:
            data.doctor_image = new
        else:
            data.doctor_image = old

        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('doctor-update-profile')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('doctor-update-profile')

        if not re.match(r'^[A-Za-z ]+$', hname):
            messages.error(request,"Hosptial name allows only letters and spaces")
            return redirect('doctor-update-profile')

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('doctor-update-profile')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', uname):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('doctor-update-profile')

        if len(uname) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('doctor-update-profile')

 
        

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('doctor-update-profile')

        if not re.match(r'^[A-Za-z.\s]+$', qual):
            messages.error(request,"Qualification allows only letters, dots(.) and spaces")
            return redirect('doctor-update-profile')

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email):

            messages.error(request,"Enter valid email")
            return redirect('doctor-update-profile')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('doctor-update-profile')
        


  
        if User.objects.filter(username=uname).exclude(id=user.id).exists():
            messages.error(request,"Username already exists")
            return redirect('doctor-update-profile')


        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request,"Email already exists")
            return redirect('doctor-update-profile')


        if DoctorModel.objects.filter(doctor_phone=phone).exclude(admin=user).exists() or PatientModel.objects.filter(patient_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('doctor-update-profile')






        user.username = uname
        user.email = email
        user.first_name = fname
        user.last_name = lname
        user.save()


        if dept_id:
            data.department = Department.objects.get(id=dept_id)

        data.doctor_address = address
        data.doctor_phone = phone
        data.qulification = qual
        data.hospital_name = hname
        data.doctor_gender = gender
        data.save()

        messages.success(request,'Update Profile Successfully')
        return redirect('D-profile')

def update_doctor_password(request):
    return render(request,'doctor/doctor-reset-password.html')

@login_required
def update_doctor_password_data(request):

    user = request.user

    if request.method == "POST":

        new_password = request.POST.get("npassword")
        confirm_password = request.POST.get("cpassword")

        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match")
            return redirect("update-doctor-password")
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect("update-doctor-password")

        # uppercase check
        if not re.search(r'[A-Z]', new_password):
            messages.error(request, "Password must contain at least 1 capital letter")
            return redirect("update-doctor-password")

        # number check
        if not re.search(r'\d', new_password):
            messages.error(request, "Password must contain at least 1 number")
            return redirect("update-doctor-password")

        # symbol check (# or @ only)
        if not re.search(r'[ #@ ]', new_password):
            messages.error(request, "Password must contain at least 1 symbol (# or @)")
            return redirect("update-doctor-password")
        
        # Password match
        if new_password == confirm_password:

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            subject = "Password Changed"

            message = (
                f"Dear {user.first_name},\n"
                f"Password :  {confirm_password},\n"
                f"Your password changed successfully."
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

           
            messages.success(request,'Reset Password Successfully')
            return redirect("logout")

        else:

             
            return redirect("update-doctor-password")

    return redirect("update-doctor-password")

def view_today_appointments(request):
    user = request.user
    doctor = DoctorModel.objects.get(admin=user)
    today= date.today()
    data = AppointmentModel.objects.filter(Doctor=doctor,appointment_date=today,status='Approved',consultation_status='pending')
    return render(request,'doctor/doctor-today-appointments.html',{'datas':data})

def consultation_form(request,pk):
    data = AppointmentModel.objects.get(id=pk)
    return render(request,'doctor/consulation-form.html',{'data':data})

def consulted(request,pk):
    user = request.user
    appointment = AppointmentModel.objects.get(id=pk)
    
    doctor = DoctorModel.objects.get(admin=user)
    if request.method == 'POST':
        diagnosis = request.POST['diagnosis']
        prescription = request.POST['prescription']
        notes = request.POST['notes']

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', diagnosis):
            messages.error(request,"Diagnosis Field contains invalid characters")
            return redirect('consultation-form',pk=pk)
        
        if not re.match(r'^[A-Za-z0-9\s.,-]+$', prescription):
            messages.error(request,"Prescription Field contains invalid characters")
            return redirect('consultation-form',pk=pk)

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', notes):
            messages.error(request,"Notes feild contains invalid characters")
            return redirect('consultation-form',pk=pk)



        patient_name = f"{appointment.patient.admin.first_name} {appointment.patient.admin.last_name}"
        doctor_name = f"{appointment.Doctor.admin.first_name} {appointment.Doctor.admin.last_name}"
        appointment.consultation_status = "CONSULATED"
        appointment.save()

        ConsultationModels.objects.create(diagnosis=diagnosis,
                                          patient_name=patient_name,
                                          doctor_name = doctor_name,
                                                      prescription=prescription,
                                                      notes=notes,
                                                      appointment=appointment,
                                                      doctor=doctor,
                                                      patient=appointment.patient,
                                                      )
        send_mail(
        "Consultation Completed",

        f"""
        Dear {appointment.patient.admin.first_name},

        Your consultation for the appointment on
        {appointment.appointment_date}
        has been completed successfully.

        Please login and check your Dashboard → My Appointments
        for consultation details and updates.

        Thank you for visiting.

        Hospital Management
        """,

        settings.EMAIL_HOST_USER,
        [appointment.patient.admin.email],
        fail_silently=False
    )

        messages.success(request,"Submited Consulted Form Successfully")
        return redirect('view-today-appointment')

def view_upcoming_appointments(request):
    user = request.user
    doctor = DoctorModel.objects.get(admin=user)

    today = date.today()

    data = AppointmentModel.objects.filter(Doctor=doctor,appointment_date__gt=today,status='Approved').order_by('appointment_date')

    return render(request, 'doctor/doctor-upcoming-appointments.html', {'datas': data})

def appointment_histroy(request):
    user = request.user
    doctor = DoctorModel.objects.get(admin=user)
    data = AppointmentModel.objects.filter(Doctor=doctor,consultation_status__in=['CONSULATED','Not Consulted'])
    return render(request, 'doctor/doctor-appointments-histroy.html', {'datas': data})

def patient_details(request):
    user = request.user

    doctor = DoctorModel.objects.get(admin=user)
    datas = PatientModel.objects.filter(
        appointmentmodel__Doctor=doctor,
        appointmentmodel__status='Approved',
    ).distinct()


    return render(request,'doctor/patient-details.html',{'datas': datas})

def not_consulted(request,pk):
    datas = AppointmentModel.objects.get(id=pk)
    return render(request,'doctor/not-consultated.html',{'data':datas})

def not_consulted_submit(request,pk):

    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":

        reason = request.POST['reason']

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', reason):
            messages.error(request,"Reason Field contains invalid characters")
            return redirect('not-consulted', pk=pk)

        
        # Create if not exists
        consultation, created = ConsultationModels.objects.get_or_create(
            appointment=appointment
        )

        consultation.reason = reason
        consultation.save()

        appointment.consultation_status = "Not Consulted"
        appointment.save()
        
        send_mail(
        "Consultation Status Update",

        f"""
        Dear {appointment.patient.admin.first_name},

        Your appointment on
        {appointment.appointment_date}
        was marked as Not Consulted.

        Please login and check your Dashboard → My Appointments
        for more details.

        Hospital Management
        """,

        settings.EMAIL_HOST_USER,
        [appointment.patient.admin.email],
        fail_silently=False
    )

        messages.success(
            request,
            "Not Consulted Form Submitted Successfully"
        )

        return redirect('view-today-appointment')
    
 
from django.utils import timezone

def doctor_dashboard(request):

    user = request.user

    doctor = DoctorModel.objects.get(
        admin=user
    )

    today = timezone.now().date()

    appointments = AppointmentModel.objects.filter(
        Doctor=doctor
    )

    appointment = AppointmentModel.objects.filter(status='Approved',Doctor=doctor)

    # CARD 1
    total_appointments = appointments.filter(status='Approved').count()

    # CARD 2
    pending_appointments = appointment.filter(consultation_status='pending').count()

    # CARD 3
    consulted_appointments = appointments.filter(
        consultation_status="CONSULATED"
    ).count()

    
    # CARD 4
    today_appointments = appointment.filter(appointment_date=today).count()

    # CARD 5
    upcoming_appointments = appointments.filter(
        appointment_date__gt=today
    ).count()

    # CARD 6
    total_patients = appointment.values(
    'patient'
).distinct().count()

    context = {

        "total_appointments":total_appointments,

        "pending_appointments":pending_appointments,

        "consulted_appointments":consulted_appointments,

        "today_appointments":today_appointments,

        "upcoming_appointments":upcoming_appointments,

        "total_patients":total_patients,

        "appointments":appointments,
    }

    return render(
        request,
        'doctor/doctor-dashboard.html',
        context
    )

def doctor_notifications(request):

    if request.user.is_authenticated:

        try:
            doctor = DoctorModel.objects.get(admin=request.user)

            today = date.today()

            return {
                'today_count':
                AppointmentModel.objects.filter(
                    Doctor=doctor,
                    appointment_date=today,
                    status='Approved',
                    consultation_status = 'pending'
                ).count(),
            }

        except:
            return {}

    return {}