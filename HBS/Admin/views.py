from django.shortcuts import render,redirect
from Admin.models import Department
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from Home.models import QueryModel,PatientModel,DoctorModel
from patient.models import AppointmentModel
from doctor.models import ConsultationModels
import random
from django.utils import timezone
from datetime import datetime
from datetime import date
from django.contrib.auth.models import auth , User
import re


# Create your views here.

def A_profile(request):
    patient = PatientModel.objects.all().count()
    doctor = DoctorModel.objects.filter(action='Approved').count()
    dep = Department.objects.all().count()
    return render(request,'admin/profile.html',{'patient':patient,
                                                'doctor':doctor,
                                                'dep':dep})

def add_department(request):
    
    return render(request,'admin/add-department.html')

def notification(request):
    return render(request,'admin/messages.html')

def querys(request):
    queries = QueryModel.objects.filter(action='pending')
    return render(request,'admin/querys.html',{'queries':queries})

def query_replay(request,pk):
    data = QueryModel.objects.get(id=pk)
    return render(request,'admin/replay.html',{'data':data})

def send_replay(request,pk):
    data = QueryModel.objects.get(id=pk)

    if request.method == 'POST':
        message = request.POST['message']

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', message):
            messages.error(request,"Message contains invalid characters")
            return redirect('replay',pk=pk)

        subject = "Replay Your Query "
        message = message
        recipient = data.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
        data.action = 'Replay'
        data.save()
        messages.success(request,'Replay Send Successfully')
        return redirect('querys_page')        


def patient_requests(request):
    patient_data = PatientModel.objects.filter(action='pending')
    return render(request,'admin/p-requests.html',{'p_datas':patient_data})


def approve_patient_request(request,pk):

    patient = PatientModel.objects.get(id=pk)

    # Existing user linked with doctor
    user = patient.admin
    fname = patient.admin.first_name
    email = patient.admin.email
    username = patient.admin.username

    last = PatientModel.objects.exclude(patient_id__isnull=True).order_by('-id').first()
    if last:
            number = int(last.patient_id[3:]) + 1
    else:
            number = 1

    patient_id = f"PAT{number:03d}"
    # Generate random password
    password = str(random.randint(100000,999999))

    # Set password for existing user
    user.set_password(password)
    user.save()

    # Approve doctor
    patient.patient_id = patient_id
    patient.action = "Approved"
    patient.save()

    subject = "Patient Registration Successful"

    message = f"""Hello {fname},Your registration request has been submitted.\n Patient ID : {patient_id} \n Username : {username} \n Password : {password} \n Thank You \n Hospital Management System"""

    recipient = email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
    messages.success(request,'Approved Patient Request Successfully')
    return redirect("patient-requests")

def reject_patient_request(request,pk):
    patient = PatientModel.objects.get(id=pk)
    return render(request,'admin/patient-reject.html',{'data':patient})    

def patient_request_replay(request, pk):

    patient = PatientModel.objects.get(id=pk)

    if request.method == 'POST':

        admin_message = request.POST['message']

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', admin_message):
            messages.error(request,"Message contains invalid characters")
            return redirect('request-reject',pk=pk)

        patient.action = 'Rejected'
        patient.save()

        subject = "Patient Registration Rejected"

        message = f"""Hello {patient.admin.first_name},\n Your registration request has been rejected.\n Reason:{admin_message} \n Thank You, \n Hospital Management System"""
        recipient = patient.admin.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
        messages.error(request,"Rejected Patient Request")
        return redirect('patient-requests')


def doctor_requests(request):
    doctor_data = DoctorModel.objects.filter(action='pending')
    return render(request,'admin/d-requests.html',{'d_datas':doctor_data})

 

def approve_request(request, pk):

    doctor = DoctorModel.objects.get(id=pk)

    # Existing user linked with doctor
    user = doctor.admin

    # Generate random password
    password = str(random.randint(100000,999999))

    # Set password for existing user
    user.set_password(password)
    user.save()

    # Approve doctor
    doctor.action = "approved"
    doctor.save()

    subject = "Doctor Registration Approved"

    message = f"""Hello {user.first_name},\n Your registration request has been approved. \n Username : {user.username} \n Password : {password} \n You can now login to the Hospital Management System.\n Thank You,\n Hospital Management System"""
    recipient = user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
    messages.success(request,'Approved Doctor Request Successfully')
    return redirect("doctor-requests")

def request_reject(request,pk):
    doctor  = DoctorModel.objects.get(id=pk)
    return render(request,'admin/reject.html',{'data':doctor})

def request_replay(request, pk):

    doctor = DoctorModel.objects.get(id=pk)

    if request.method == 'POST':

        admin_message = request.POST['message']

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', admin_message):
            messages.error(request,"Message contains invalid characters")
            return redirect('request-reject',pk=pk)

        doctor.action = 'Rejected'
        doctor.save()

        subject = "Doctor Registration Rejected"

        message = f"""Hello {doctor.admin.first_name},\n Your registration request has been rejected.\n Reason:{admin_message} \n Thank You, \n Hospital Management System"""
        recipient = doctor.admin.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
        messages.error(request,"Rejected Doctor Request")
        return redirect('doctor-requests')



def add_department_data(request):
    
    if request.method == "POST":
        dep = request.POST['dep']
        desc = request.POST['desc']

        if not re.match(r'^[A-Za-z ]+$', dep):
            messages.error(request,"Department allows only letters and spaces")
            return redirect('add-department')
        
        if not re.match(r'^[A-Za-z0-9\s.,-]+$', desc):
            messages.error(request,"Description contains invalid characters")
            return redirect('add-department')

        if Department.objects.filter(dep_name=dep).exists():
            messages.error(request,"Department  already exists")
            return redirect('add-department')
        
        dept = Department(
            dep_name=dep,
            desc=desc
        )
        dept.save()
        
        messages.success(request,'Add Department Successfully')
     
        return redirect("view-department")
     

def view_department(request):
    dept = Department.objects.all()
    return render(request,'admin/view-department.html',{'dept':dept})

def edit_department(request,pk):
    dept = Department.objects.get(id=pk)
    return render(request,'admin/edit-department.html',{'dept':dept})

def edit_department_data(request,pk):
    dept = Department.objects.get(id=pk)
    if request.method == 'POST':
        dep = request.POST['dep']
        desc = request.POST['desc']

        if not re.match(r'^[A-Za-z ]+$', dep):
            messages.error(request,"Department allows only letters and spaces")
            return redirect('edit-department',pk=pk)
        
        if not re.match(r'^[A-Za-z0-9\s.,-]+$', desc):
            messages.error(request,"Description contains invalid characters")
            return redirect('edit-department',pk=pk)

        if Department.objects.filter(dep_name=dep).exclude(id=pk).exists():
            messages.error(request,"Department  already exists")
            return redirect('edit-department',pk=pk)
        
        dept.dep_name = dep
        dept.desc = desc
        
        dept.save()
        messages.info(request,'Edit Department Successfully')
        return redirect('view-department')
    
def delete_department(request,pk):
    dept = Department.objects.get(id=pk)
    dept.delete()
    messages.error(request,'Delete Department Successfully')
    return redirect('view-department')

def add_patient(request):
    return render(request,'admin/add-patient.html')

def view_patient(request):
    data =  PatientModel.objects.filter(action='Approved')
    return render(request,'admin/view-patient.html',{'datas':data})

def delete_patient(request,pk):

    data = PatientModel.objects.get(id=pk)
    admin = data.admin
    admin.delete()
    data.delete()
    messages.error(request,'Delete Patient Successfully')
    return redirect('view-patient')

def add_doctor(request):
    dept = Department.objects.all()
    return render(request,'admin/add-doctor.html',{'depts':dept})

def view_doctor(request):
    data =  DoctorModel.objects.filter(action='approved')
    return render(request,'admin/view-doctor.html',{'datas':data})

def delete_doctor(request,pk):
    data = DoctorModel.objects.get(id=pk)
    
    admin = data.admin
    admin.delete()
    data.delete()
    messages.error(request,'Delete Doctor Successfully')
    return redirect('view-doctor')

def view_appointments(request):

    data = AppointmentModel.objects.filter(status='Pending')
   
    return render(request,'admin/view-appointment.html',{'datas':data})

 

def approve_appointment(request, pk):
    
    appointment = AppointmentModel.objects.get(id=pk)

    doctor = appointment.Doctor
    date = appointment.appointment_date
    


    # Check same time slot already approved
    # slot_exists = AppointmentModel.objects.filter(
    #     Doctor=doctor,
    #     appointment_date=date,
    #     status='Approved'
    # ).exclude(id=appointment.id).exists()


    # if slot_exists:

    #     messages.error(request,"This time slot already booked")
    #     return redirect('view-appointments')

    # Doctor daily limit
    total = AppointmentModel.objects.filter(Doctor=doctor,appointment_date=date,status='Approved').count()

    if total >= 5:

        messages.error(request,"Doctor not available today. Daily limit reached")
        return redirect('view-appointments')


    appointment.status = "Approved"
    appointment.save()

    

    send_mail(
        "Appointment Approved",

        f"""
        Dear {appointment.patient.admin.first_name},

        Your appointment has been approved.

        Doctor : Dr. {appointment.Doctor.admin.first_name}
        Department : {appointment.department.dep_name}
        Date : {appointment.appointment_date}
        

        Please visit the hospital on the scheduled date.

        Thank You
        Hospital Management
""",

        settings.EMAIL_HOST_USER,
        [appointment.patient.admin.email],
        fail_silently=False
    )



    messages.success(request,"Appointment approved successfully")
    return redirect('view-appointments')

def reject_appointment(request,pk):
    data = AppointmentModel.objects.get(id=pk)
    return render(request,'admin/reject-appointment.html',{'data':data})

def reject_appointment_data(request, pk):

    appointment = AppointmentModel.objects.get(id=pk)

    if request.method == "POST":

        reason = request.POST['reason']
        s_date = request.POST['s_date']
         


        if not re.match(r'^[A-Za-z0-9\s.,-]+$', reason):
            messages.error(request,"Reason feild contains invalid characters")
            return redirect('request-reject',pk=pk)



        send_mail(
        "Appointment Rejected",

        f"""
        Dear {appointment.patient.admin.first_name},

        We regret to inform you that your appointment scheduled on
        {appointment.appointment_date} has been rejected.

        Suggested Date : {s_date}
        Reason  : {reason}

        Please book another appointment.

        Thank You
        Hospital Management
        """,

        settings.EMAIL_HOST_USER,[appointment.patient.admin.email],fail_silently=False
    )
        
        
        appointment.status='Rejected'
        appointment.consultation_status = 'Rejected'

        appointment.rejected_reason=reason

        appointment.suggested_date=s_date


        appointment.save()

        messages.error(request,"Appointment rejected")

        return redirect('view-appointments')
    
def Consultation_status(request):

     
    datas = AppointmentModel.objects.filter(status="Approved")
    consultations = ConsultationModels.objects.filter(
        appointment__in=datas
    )
    return render(request,'admin/consultation_status.html',{'datas':datas,
        'consultations': consultations})

def add_patient_data(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob =  request.POST.get('dob')
        gender = request.POST['gender']
        blood = request.POST['blood']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        image=request.FILES.get('file')

        if image==None:
            image="images/default.png"
        action = "Approved"

       

        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('add-patient')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('add-patient')



        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('add-patient')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', username):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('add-patient')

        if len(username) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('add-patient')

 

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('add-patient')

 

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email):

            messages.error(request,"Enter valid email")
            return redirect('add-patient')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('add-patient')
        

        try:

            dob = datetime.strptime(dob, '%Y-%m-%d').date()

            today = date.today()

            if dob > today:
                messages.error(request,"Date of birth cannot be future date")
                return redirect('add-patient')

            age = today.year - dob.year - ((today.month,today.day)<(dob.month,dob.day))

            if age < 0:
                messages.error(request,"Invalid date of birth")
                return redirect('add-patient')

        except:
            messages.error(request,"Invalid date format")
            return redirect('add-patient')


  
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('add-patient')


        if User.objects.filter(email=email).exists() :
            messages.error(request,"Email already exists")
            return redirect('add-patient')


        if PatientModel.objects.filter(patient_phone=phone).exists() or DoctorModel.objects.filter(doctor_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('add-patient')


        age = date.today().year - dob.year
        
        last = PatientModel.objects.exclude(patient_id__isnull=True).order_by('-id').first()


        if last:
            number = int(last.patient_id[3:]) + 1
        else:
            number = 1

        patient_id = f"PAT{number:03d}"
        # Generate random 6 digit password
        password = str(random.randint(100000,999999))

        user = User.objects.create_user(first_name=fname,
                                        last_name=lname,
                                        email = email,
                                        username=username,
                                        password=password)
        user.save()
        
        user_data = User.objects.get(id=user.id)

        patient_data = PatientModel(patient_id=patient_id,
                                    patient_gender = gender,
                                    patient_blood_group = blood,
                                    patient_address = address,
                                    patient_phone = phone,
                                    patient_image = image,
                                    patient_age=age,
                                    action = action,
                                    admin = user_data)

        patient_data.save()

        # Email content
        subject = "Patient Registration Successful"

        message = f"""Hello {fname},Your registration request has been submitted.\n Patient ID : {patient_id} \n Username : {username} \n Password : {password} \n Thank You \n Hospital Management System"""

        recipient = email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
        messages.success(request,'Add Patient Successfully')
        return redirect("view-patient")
    else:
         return redirect('add-patient')
    
def add_doctor_data(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        uname = request.POST['uname']
        qual = request.POST['qual']
        yoe = request.POST['yoe']
        hname = request.POST['hname']
        mregno = request.POST['mregno']
        select = request.POST['select']


        

        image=request.FILES.get('file')
        if image==None:
            image="images/default.png"

        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('add-doctor')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('add-doctor')

        if not re.match(r'^[A-Za-z ]+$', hname):
            messages.error(request,"Hosptial name allows only letters and spaces")
            return redirect('add-doctor')

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('add-doctor')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', uname):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('add-doctor')

        if len(uname) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('add-doctor')

 
        if not re.match(r'^\d{6}$', mregno):
            messages.error(request,"Medical number must contain exactly 6 digits")
            return redirect('add-doctor')

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('add-doctor')

        if not re.match(r'^[A-Za-z.\s]+$', qual):
            messages.error(request,"Qualification allows only letters, dots(.) and spaces")
            return redirect('add-doctor')

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email):

            messages.error(request,"Enter valid email")
            return redirect('add-doctor')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('add-doctor')
        

        try:

            dob = datetime.strptime(dob,'%Y-%m-%d').date()

            today = date.today()

            if dob > today:
                messages.error(request,"Date of birth cannot be future date")
                return redirect('add-doctor')

            age = today.year - dob.year - ((today.month,today.day)<(dob.month,dob.day))

            if age < 18:
                messages.error(request,"Invalid date of birth")
                return redirect('add-doctor')

        except:
            messages.error(request,"Invalid date format")
            return redirect('add-doctor')


  
        if User.objects.filter(username=uname).exists():
            messages.error(request,"Username already exists")
            return redirect('add-doctor')


        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('add-doctor')


        if DoctorModel.objects.filter(doctor_phone=phone).exists() or PatientModel.objects.filter(patient_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('add-doctor')
        
        if DoctorModel.objects.filter(mrgno=mregno).exists():
            messages.error(request,"Medical Medical Registration Number already exists")
            return redirect('add-doctor')

        # Generate random password
        password = str(random.randint(100000,999999))

        

        age = date.today().year - dob.year

        user = User.objects.create_user(first_name=fname,
                                        last_name=lname,
                                        email = email,
                                        username=uname,
                                        password=password)
        user.save()

        user_data = User.objects.get(id=user.id)
        dept = Department.objects.get(id=select)
        action = "approved"
        doctor_data =DoctorModel(doctor_age=age,
                                 doctor_gender = gender,
                                 doctor_address = address,
                                 doctor_phone = phone,
                                 doctor_image = image,
                                 mrgno = mregno,
                                 qulification = qual,
                                 YOE = yoe,
                                 hospital_name = hname,
                                 action = action,
                                 admin = user_data,
                                 department = dept)
        doctor_data.save()
         

        subject = "Doctor Registration Successfully"

        message = f"""Hello {user.first_name},\n Your registration has Successed. \n Username : {user.username} \n Password : {password} \n You can now login to the Hospital Management System.\n Thank You,\n Hospital Management System"""
        recipient = user.email
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
        messages.success(request,'Add Doctor Successfully')
        return redirect("view-doctor")

def admin_dashboard(request):

    total_patients = PatientModel.objects.filter(action='Approved').count()
    total_doctors = DoctorModel.objects.filter(action='approved').count()
    total_appointments = AppointmentModel.objects.count()
    

    pending_appointments = AppointmentModel.objects.filter(status="Pending").count()
    completed_consultations = AppointmentModel.objects.filter(consultation_status='CONSULATED').count()

    today = timezone.now().date()
    today_appointments = AppointmentModel.objects.filter(appointment_date=today).count()


    doctors = DoctorModel.objects.filter(action='Approved')

    department_id = request.GET.get("department")
    doctor_id = request.GET.get("doctor")

    # ALL DEPARTMENTS
    departments = Department.objects.all()

    # STEP 1: FILTER DOCTORS BY DEPARTMENT
    doctors = DoctorModel.objects.none()

    if department_id:
        doctors = DoctorModel.objects.filter(
            department_id=department_id,
            action='Approved'
        )

    # STEP 2: SELECTED DOCTOR DETAILS
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
                status='Approved'
            ).count()

            d.remaining_slots = 5 - d.today_count
        
    context = {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "completed_consultations": completed_consultations,
        "today_appointments": today_appointments,
        "doctor":doctors,
        "departments": departments,
        "doctor": doctors,
        "selected_doctor": selected_doctor,
    }

    return render(request, "admin/admin-dashboard.html", context)

 

def admin_notifications(request):

    doctor_pending = DoctorModel.objects.filter(action='Pending').count()

    patient_pending = PatientModel.objects.filter(action='Pending').count()

    appointment_pending = AppointmentModel.objects.filter(
        status='Pending'
    ).count()

    query_pending = QueryModel.objects.filter(
        action='Pending'
    ).count()

    total_pending = (
        doctor_pending +
        patient_pending +
        appointment_pending +
        query_pending
    )

    return {
        'doctor_pending':doctor_pending,
        'patient_pending':patient_pending,
        'appointment_pending':appointment_pending,
        'query_pending':query_pending,
        'total_pending':total_pending,
    }