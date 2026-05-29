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
import re
from datetime import datetime, date, time
from Admin.models import Department
from django.utils import timezone

# Create your views here.

def patient_profile(request):
    user=request.user
    data = PatientModel.objects.get(admin=user)
     

    return render(request,'patient/patient-profile.html',{'data':data})

def update_profile(request):
    user = request.user
    data = PatientModel.objects.get(admin=user)
    return render(request,'patient/update-profile.html',{'data':data})

def update_patient_profile_data(request):
    user = request.user
    data = PatientModel.objects.get(admin=user)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        
        gender = request.POST['gender']
        blood = request.POST['blood']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']

        old = data.patient_image
        new = request.FILES.get("file")

        # image update
        if new:
            data.patient_image = new
        else:
            data.patient_image = old

        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('update-profile')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('update-profile')



        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('update-profile')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', username):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('update-profile')

        if len(username) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('update-profile')

 

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('update-profile')

 

        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',email):
            messages.error(request,"Enter valid email")
            return redirect('update-profile')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('update-profile')
        

       
       
  
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request,"Username already exists")
            return redirect('update-profile')


        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request,"Email already exists")
            return redirect('update-profile')


        if PatientModel.objects.filter(patient_phone=phone).exclude(admin=user).exists()  or DoctorModel.objects.filter(doctor_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('update-profile')

        # update USER table
        
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.username = username
        user.save()

        # update PATIENT table
        
        data.patient_gender = gender
        data.patient_blood_group = blood
        data.patient_address = address
        data.patient_phone = phone
        data.patient_gender = gender

        data.save()
        messages.info(request,'Update Profile Successfully')
        return redirect("P-profile")

def patient_reset_password(request):
    return render(request,'patient/patient-reset-password.html')

@login_required
def update_patient_password(request):

    user = request.user

    if request.method == "POST":

        new_password = request.POST.get("npassword")
        confirm_password = request.POST.get("cpassword")

        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match")
            return redirect("patient-password")
        
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect("patient-password")

        # uppercase check
        if not re.search(r'[A-Z]', new_password):
            messages.error(request, "Password must contain at least 1 capital letter")
            return redirect("patient-password")

        # number check
        if not re.search(r'\d', new_password):
            messages.error(request, "Password must contain at least 1 number")
            return redirect("patient-password")

        # symbol check (# or @ only)
        if not re.search(r'[ #@ ]', new_password):
            messages.error(request, "Password must contain at least 1 symbol (# or @)")
            return redirect("patient-password")
        
        
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

             
            return redirect("patient-reset-password")

    return redirect("patient-reset-password")

def booking_appointment(request):
    user=request.user
    doctor = DoctorModel.objects.filter(action='Approved')
    patient = PatientModel.objects.get(admin=user)
    
    return render(request,"patient/booking-appointment.html",{'doctor':doctor,
                                                              'patient':patient})

 


def booking_appointment_data(request):

    user = request.user
    patient = PatientModel.objects.get(admin=request.user)


    
    if request.method == 'POST':

        doctor_id = request.POST['doctor']
        ap_date = request.POST['appointment_date']
        symptoms = request.POST['symptoms']
       

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', symptoms):
            messages.error(request,"Symptoms contains invalid characters")
            return redirect('booking-appointment')

        doctor= DoctorModel.objects.filter(id=doctor_id).first()
        if not doctor:
            messages.error(request, "Invalid doctor selected")
            return redirect('booking-appointment')
        
        try:
            ap_date_obj = datetime.strptime(ap_date, "%Y-%m-%d").date()
        except:
            messages.error(request, "Invalid date or time format")
            return redirect('booking-appointment')


        today = date.today()
        
        #  Past date check
        if ap_date_obj < today:
            messages.error(request, "Appointment date cannot be in the past")
            return redirect('booking-appointment')

        appointment_count = AppointmentModel.objects.filter(patient=patient,
                                                            Doctor=doctor,
                                                            appointment_date=ap_date).count()
        

        if appointment_count >= 1:
            messages.error(request,"You already booked an appointment with this doctor today.")
            return redirect('booking-appointment')

        patient_name = f"{patient.admin.first_name} {patient.admin.last_name}"
        doctor_name = f"{doctor.admin.first_name} {doctor.admin.last_name}"
        patient_age = patient.patient_age
        # doctor's department automatically
        department = doctor.department

        last = AppointmentModel.objects.order_by('-id').first()
        if last:
            number = int(last.appointment_id[3:]) + 1
        else:
            number = 1

        appointment_id = f"APT{number:03d}"

        AppointmentModel.objects.create(
            patient=patient,
            Doctor=doctor,
            patient_name = patient_name,
            doctor_name = doctor_name,
            department=department,
            appointment_date=ap_date,
            symptoms=symptoms,
            status='Pending',
            patient_age=patient_age,
            appointment_id = appointment_id,
        )

        messages.success(request,'Book appointment Succesfully')
        return redirect('my-appointments')

     
    return redirect('booking-appointment')

def my_appointment(request):
    user = request.user

    patient = PatientModel.objects.get(admin=user)

    # Today appointments
    datas = AppointmentModel.objects.filter(patient=patient).order_by('-created_at')

    # Consultation data (all or filter if needed)
    consultations = ConsultationModels.objects.filter(
        appointment__in=datas
    )
    
    return render(request, 'patient/my-appointments.html', {
        'datas':datas,
        'consultations': consultations
    })

def appointment_histroy(request):
    user = request.user
    patient = PatientModel.objects.get(admin=user)
    data = AppointmentModel.objects.filter(patient=patient)
    consultations = ConsultationModels.objects.filter(patient=patient)
    return render(request,'patient/appointment-histroy.html',{'datas':data,
                                                               'consultations': consultations})


def patient_dashboard(request):

    user = request.user

    # current patient
    patient = PatientModel.objects.get(admin=user)

    today = timezone.now().date()

    # ==========================
    # Dashboard cards
    # ==========================

    appointments = AppointmentModel.objects.filter(
        patient=patient
    )

    total_appointments = appointments.count()

    pending_appointments = appointments.filter(
        status='Pending'
    ).count()

    rejected_appointments = appointments.filter(status='Rejected').count()
    approved_appointments = appointments.filter(status='Approved').count()

    completed_appointments = AppointmentModel.objects.filter(
        patient=patient,consultation_status="CONSULATED"
    ).count()

    today_appointments = appointments.filter(
        appointment_date=today
    ).count()

    # ==========================
    # Department → Doctor filter
    # ==========================

    department_id = request.GET.get("department")
    doctor_id = request.GET.get("doctor")

    departments = Department.objects.all()

    doctors = DoctorModel.objects.none()

    if department_id:
        doctors = DoctorModel.objects.filter(
            department_id=department_id,
            action='Approved'
        )
    

    # ==========================
    # Selected doctor details
    # ==========================

    selected_doctor = None

    if doctor_id:

        selected_doctor = DoctorModel.objects.filter(
            id=doctor_id,
            action='Approved'
        )

        for d in selected_doctor:

            d.today_count = AppointmentModel.objects.filter(
                Doctor=d,
                appointment_date=today,
                status='Approved',
            ).count()

            d.remaining_slots = 5 - d.today_count

            if d.remaining_slots < 0:
                d.remaining_slots = 0

    context = {

        # dashboard cards
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'today_appointments': today_appointments,
        'rejected_appointments': rejected_appointments,
        'approved_appointments': approved_appointments,


        # dropdowns
        'departments': departments,
        'doctor': doctors,

        # selected doctor
        'selected_doctor': selected_doctor,
    }

    return render(
        request,
        'patient/patient-dashboard.html',
        context
    )

 