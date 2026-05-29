 

document.getElementById("patientForm").addEventListener("submit", function(e){
        e.preventDefault();

    // clear errors
    document.getElementById("fnameError").innerHTML="";
    document.getElementById("lnameError").innerHTML="";
    document.getElementById("addressError").innerHTML="";
    document.getElementById("phoneError").innerHTML="";
    document.getElementById("emailError").innerHTML="";
    document.getElementById("usernameError").innerHTML="";
    document.getElementById("imageError").innerHTML="";

    let fname=document.getElementById("fname").value.trim();
    let lname=document.getElementById("lname").value.trim();
    let address=document.getElementById("address").value.trim();
    let phone=document.getElementById("phone").value.trim();
    let email=document.getElementById("email").value.trim();
    let username=document.getElementById("username").value.trim();
    let image=document.getElementById("image").files[0];

    let isValid=true;

    // Only letters
    let namePattern=/^[A-Za-z ]+$/;

    // Username letters+numbers+symbols
    let usernamePattern=/^[A-Za-z0-9@._-]+$/;

    // Phone
    let phonePattern=/^[0-9]{10}$/;

    // Email
    let emailPattern=/^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,}$/;


    // First Name
    if(!namePattern.test(fname)){
        document.getElementById("fnameError").innerHTML = "Only letters allowed";
    isValid=false;
    }

    // Last Name
    if(!namePattern.test(lname)){
        document.getElementById("lnameError").innerHTML = "Only letters allowed";
    isValid=false;
    }

    // Address
    if(!namePattern.test(address)){
        document.getElementById("addressError").innerHTML =
        "Address only letters allowed";
    isValid=false;
    }

    // Phone
    if(!phonePattern.test(phone)){
        document.getElementById("phoneError").innerHTML =
        "Enter valid 10 digit number";
    isValid=false;
    }

    // Email
    if(!emailPattern.test(email)){
        document.getElementById("emailError").innerHTML =
        "Enter valid email";
    isValid=false;
    }

    // Username
    if(!usernamePattern.test(username)){
        document.getElementById("usernameError").innerHTML =
        "Letters, numbers and symbols allowed";
    isValid=false;
    }

    // Image
    if(image){

        let allowed=["image/jpeg","image/png","image/jpg"];

    if(!allowed.includes(image.type)){
        document.getElementById("imageError").innerHTML =
        "Only JPG and PNG allowed";
    isValid=false;
        }

        if(image.size>2*1024*1024){
        document.getElementById("imageError").innerHTML =
        "Image below 2MB";
    isValid=false;
        }
    }

    if(isValid){
        alert("Registration Submitted Successfully");
    this.submit();
    }

});