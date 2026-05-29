from django.shortcuts import render, redirect
from django.contrib.auth.models import auth , User
from Home.models import PatientModel,DoctorModel,QueryModel
from django.conf import settings
from django.core.mail import send_mail
import random
from datetime import datetime
from datetime import date
from Admin.models import Department
from django.contrib import messages
import re

def home(request):
    return render(request,'home/home.html')


def about(request):
    return render(request,'home/about.html')

def login(request):
    return render(request,"home/login.html")

def contact(request):
    return render(request,'home/contact.html')

def patient(request):
    return render(request,"home/patient-register.html")

def doctor(request):
    dept = Department.objects.all()
    return render(request,'home/doctor-register.html',{'dept':dept})

def login_data(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not re.match(r'^[A-Za-z0-9$#]+$', username):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('login')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            if user.is_superuser:
                messages.success(request,f"{user.username} Login Successfully")
                return redirect('admin-dashboard')

        
            elif PatientModel.objects.filter(admin=user).exists():
                messages.success(request,f"{user.username} Login Successfully")
                return redirect("patient-dashboard")

             
            elif DoctorModel.objects.filter(admin=user).exists():
                messages.success(request,f"{user.username} Login Successfully")
                return redirect("doctor-dashboard")

            else:
                messages.error(request,'User Not Found')
                return redirect('login')
        else:
                messages.error(request,'Invaild Username and Password')
                return redirect('login')
            
def logout(request):
    auth.logout(request)
    messages.error(request,"Logout Successfully")
    return redirect('login')


def query(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject=request.POST['subject']
        message = request.POST['message']
        action = "pending"

        query_data = QueryModel(name=name,
                                phone = phone,
                                email=email,
                                subject=subject,
                                message=message,
                                action=action)
        query_data.save()
        messages.success(request,"Send Query Successfully")
        return redirect('contact')
    return redirect('contact')

def patient_register(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST.get('dob')
        gender = request.POST['gender']
        blood = request.POST['blood']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        image=request.FILES.get('file')
        if image==None:
            image="images/default.png"
        action = "pending"


        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('patient')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('patient')



        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('patient')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', username):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('patient')

        if len(username) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('patient')

 

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('patient')

 

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email):

            messages.error(request,"Enter valid email")
            return redirect('patient')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('patient')
        

        try:

            dob = datetime.strptime(dob,'%Y-%m-%d').date()

            today = date.today()

            if dob > today:
                messages.error(request,"Date of birth cannot be future date")
                return redirect('patient')

            age = today.year - dob.year - ((today.month,today.day)<(dob.month,dob.day))

            if age <= 0:
                messages.error(request,"Invalid date of birth")
                return redirect('patient')

        except:
            messages.error(request,"Invalid date format")
            return redirect('patient')


  
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('patient')


        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('patient')


        if PatientModel.objects.filter(patient_phone=phone).exists()or DoctorModel.objects.filter(doctor_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('patient')



        age = date.today().year - dob.year
        
         

        user = User.objects.create_user(first_name=fname,
                                        last_name=lname,
                                        email = email,
                                        username=username)
        user.save()
        
        user_data = User.objects.get(id=user.id)

        patient_data = PatientModel(patient_gender = gender,
                                    patient_blood_group = blood,
                                    patient_address = address,
                                    patient_phone = phone,
                                    patient_image = image,
                                    patient_age=age,
                                    action = action,
                                    admin = user_data)

        patient_data.save()
 
         
        messages.success(request,'Your registration request has been sent successfully.Please wait for admin approval.Your login details will be sent to your email after approval.')
        return redirect('patient')
    else:
         return redirect('patient')


def doctor_register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        uname = request.POST['uname']
        qual = request.POST['qual'].strip()
        yoe = request.POST['yoe']
        hname = request.POST['hname']
        mregno = request.POST['mregno'].strip()
        select = request.POST['select']


        

        image=request.FILES.get('file')
        if image==None:
            image="images/default.png"

        if not re.match(r'^[A-Za-z ]+$', fname):
            messages.error(request,"First name allows only letters and spaces")
            return redirect('doctor')


        if not re.match(r'^[A-Za-z ]+$', lname):
            messages.error(request,"Last name allows only letters and spaces")
            return redirect('doctor')

        if not re.match(r'^[A-Za-z ]+$', hname):
            messages.error(request,"Hosptial name allows only letters and spaces")
            return redirect('doctor')

        if not re.match(r'^[A-Za-z0-9\s.,-]+$', address):
            messages.error(request,"Address contains invalid characters")
            return redirect('doctor')

 

        if not re.match(r'^[A-Za-z0-9$#]+$', uname):
            messages.error(request,"Username allows only letters,numbers,$,#")
            return redirect('doctor')

        if len(uname) < 6:
            messages.error(request,"Username must contain at least 6 characters")
            return redirect('doctor')

 
        if not re.match(r'^\d{6}$', mregno):
            messages.error(request,"Medical number must contain exactly 6 digits")
            return redirect('doctor')

        if not re.match(r'^[6-9]\d{9}$', phone):
            messages.error(request,"Enter valid mobile number")
            return redirect('doctor')

        if not re.match(r'^[A-Za-z.\s]+$', qual):
            messages.error(request,"Qualification allows only letters, dots(.) and spaces")
            return redirect('doctor')

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email):

            messages.error(request,"Enter valid email")
            return redirect('doctor')

        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$',email):
            messages.error(request,"Only Gmail addresses are allowed")
            return redirect('doctor')
        

        try:

            dob = datetime.strptime(dob,'%Y-%m-%d').date()

            today = date.today()

            if dob > today:
                messages.error(request,"Date of birth cannot be future date")
                return redirect('doctor')

            age = today.year - dob.year - ((today.month,today.day)<(dob.month,dob.day))

            if age <= 18:
                messages.error(request,"Invalid date of birth")
                return redirect('doctor')

        except:
            messages.error(request,"Invalid date format")
            return redirect('doctor')


  
        if User.objects.filter(username=uname).exists():
            messages.error(request,"Username already exists")
            return redirect('doctor')


        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('doctor')


        if DoctorModel.objects.filter(doctor_phone=phone).exists() or PatientModel.objects.filter(patient_phone=phone).exists():
            messages.error(request,"Phone number already exists")
            return redirect('doctor')

        if DoctorModel.objects.filter(mrgno=mregno).exists():
            messages.error(request,"Medical Medical Registration Number already exists")
            return redirect('doctor')

        age = date.today().year - dob.year

        user = User.objects.create_user(first_name=fname,
                                        last_name=lname,
                                        email = email,
                                        username=uname)
        user.save()

        user_data = User.objects.get(id=user.id)
        dept = Department.objects.get(id=select)

        doctor_data =DoctorModel(doctor_age=age,
                                 doctor_gender = gender,
                                 doctor_address = address,
                                 doctor_phone = phone,
                                 doctor_image = image,
                                 mrgno = mregno,
                                 qulification = qual,
                                 YOE = yoe,
                                 hospital_name = hname,
                                 action = 'pending',
                                 admin = user_data,
                                 department = dept)
        doctor_data.save()
        messages.success(request,'Your registration request has been sent successfully.Please wait for admin approval.Your login details will be sent to your email after approval.')
        return redirect('doctor')
        