document.getElementById("doctorForm").addEventListener("submit",function(e){

e.preventDefault();

// clear errors
document.getElementById("fnameError").innerHTML="";
document.getElementById("lnameError").innerHTML="";
document.getElementById("addressError").innerHTML="";
document.getElementById("phoneError").innerHTML="";
document.getElementById("emailError").innerHTML="";
document.getElementById("usernameError").innerHTML="";
document.getElementById("regnoError").innerHTML="";
document.getElementById("qualificationError").innerHTML="";
document.getElementById("hospitalError").innerHTML="";
document.getElementById("imageError").innerHTML="";

let fname=document.getElementById("fname").value.trim();
let lname=document.getElementById("lname").value.trim();
let address=document.getElementById("address").value.trim();
let phone=document.getElementById("phone").value.trim();
let email=document.getElementById("email").value.trim();
let username=document.getElementById("username").value.trim();
let regno=document.getElementById("regno").value.trim();
let qualification=document.getElementById("qualification").value.trim();
let hospital=document.getElementById("hospital").value.trim();
let image=document.getElementById("image").files[0];

let valid=true;

let namePattern=/^[A-Za-z ]+$/;
let phonePattern=/^[0-9]{10}$/;
let emailPattern=/^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,}$/;
let qualificationPattern=/^[A-Za-z., ]+$/;
let usernamePattern=/^[A-Za-z0-9@._-]+$/;


// First name
 
if(!namePattern.test(fname)){
document.getElementById("fnameError").innerHTML=
"Only letters allowed";
valid=false;
}


// Last name
 
if(!namePattern.test(lname)){
document.getElementById("lnameError").innerHTML=
"Only letters allowed";
valid=false;
}


// Address
if(!namePattern.test(address)){
document.getElementById("addressError").innerHTML=
"Only letters allowed";
valid=false;
}


// Phone
if(!phonePattern.test(phone)){
document.getElementById("phoneError").innerHTML=
"10 digits only";
valid=false;
}


// Email
if(!emailPattern.test(email)){
document.getElementById("emailError").innerHTML=
"Invalid email";
valid=false;
}


// Username
if(!usernamePattern.test(username)){
document.getElementById("usernameError").innerHTML=
"Letters numbers @._- only";
valid=false;
}


// Qualification
if(!qualificationPattern.test(qualification)){
document.getElementById("qualificationError").innerHTML=
"Only letters, comma and dot";
valid=false;
}


// Hospital
if(!namePattern.test(hospital)){
document.getElementById("hospitalError").innerHTML=
"Letters only";
valid=false;
}


// Image
if(image){

let allowed=["image/jpeg","image/png","image/jpg"];

if(!allowed.includes(image.type)){
document.getElementById("imageError").innerHTML=
"Only JPG/PNG allowed";
valid=false;
}

if(image.size>2*1024*1024){
document.getElementById("imageError").innerHTML=
"Image below 2MB";
valid=false;
}
}

if(valid){
alert("Doctor Registration Successful");
this.submit();
}

});