document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("contactForm");

    form.addEventListener("submit", function(e){

        e.preventDefault();

        let name = document.getElementById("name").value.trim();
        let phone = document.getElementById("phone").value.trim();
        let email = document.getElementById("email").value.trim();
        let subject = document.getElementById("subject").value.trim();
        let message = document.getElementById("message").value.trim();

        // clear old errors
        document.getElementById("nameError").innerText="";
        document.getElementById("phoneError").innerText="";
        document.getElementById("emailError").innerText="";
        document.getElementById("subjectError").innerText="";
        document.getElementById("messageError").innerText="";

        let valid=true;

        let namePattern=/^[A-Za-z ]+$/;
        let phonePattern=/^[6-9]\d{9}$/;
        let emailPattern=/^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        let subjectPattern=/^[A-Za-z ]+$/;
        let messagePattern=/^[A-Za-z0-9\s.,!?@#$%^&*()_+=\-:;"'<>/\\[\]{}]+$/;

        // Name
        if(!namePattern.test(name)){
            document.getElementById("nameError").innerText =
            "Only letters allowed";
            valid=false;
        }

        // Phone
        if(!phonePattern.test(phone)){
            document.getElementById("phoneError").innerText =
            "Enter valid 10-digit number";
            valid=false;
        }

        // Email
        if(!emailPattern.test(email)){
            document.getElementById("emailError").innerText =
            "Enter valid email";
            valid=false;
        }

        // Subject
        if(!subjectPattern.test(subject)){
            document.getElementById("subjectError").innerText =
            "Only letters allowed";
            valid=false;
        }

        // Message
        if(message.length < 10){
            document.getElementById("messageError").innerText =
            "Minimum 10 characters";
            valid=false;
        }

        if(valid){
            form.submit();
        }

    });

});