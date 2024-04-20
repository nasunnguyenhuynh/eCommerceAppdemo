// const forms = document.querySelector(".forms"),
//     pwShowHide = document.querySelectorAll(".eye-icon"),
//     links = document.querySelectorAll(".link");

document.getElementById("signupForm").addEventListener("submit", function (event) {
    let valid = true;
    let errors = [];
    const phoneNumber = document.getElementById("phone_number");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("retype_password");
    const errorContainer = document.getElementById("errorMessages");

    // Clear previous errors
    errorContainer.innerHTML = '';

    // Check phone number is not empty
    if (!phoneNumber || phoneNumber.value.trim() === "") {
        errors.push("Phone number is required.");
        valid = false;
    }

    // Check password requirements
    if (!password || password.value.length < 8 || !/[a-z]/.test(password.value) || !/[A-Z]/.test(password.value) || !/[0-9]/.test(password.value) || !/[!@#$%^&*(),.?":{}|<>]/.test(password.value)) {
        errors.push("Password must be at least 8 characters long and include lowercase, uppercase, numeric, and special characters.");
        valid = false;
    }

    // Check passwords match
    if (password.value !== confirmPassword.value) {
        errors.push("Passwords do not match.");
        valid = false;
    }

    // If not valid, prevent form submit and show errors
    if (!valid) {
        event.preventDefault();
        errors.forEach(function (error) {
            let div = document.createElement("div");
            div.textContent = error;
            errorContainer.appendChild(div);
        });
    }
});


document.getElementById("basicSetupProfileForm").addEventListener("submit", function (event) {
    let valid = true;
    let errors = [];
    const username = document.getElementById("username");
    const errorContainer = document.getElementById("errorMessages");

    // Clear previous errors
    errorContainer.innerHTML = '';

    // Check Username is not empty
    if (!username || username.value.trim() === "") {
        errors.push("Username is required.");
        valid = false;
    }

    if (username.indexOf(" ") !== -1) {
        errors.push("Username must not contain whitespace.");
        valid = false;
    }

    // If not valid, prevent form submit and show errors
    if (!valid) {
        event.preventDefault();
        errors.forEach(function (error) {
            let div = document.createElement("div");
            div.textContent = error;
            errorContainer.appendChild(div);
        });
    }
});

// pwShowHide.forEach(eyeIcon => {
//     eyeIcon.addEventListener("click", () => {
//         let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
//
//         pwFields.forEach(password => {
//             if (password.type === "password") {
//                 password.type = "text";
//                 eyeIcon.classList.replace("bx-hide", "bx-show");
//                 return;
//             }
//             password.type = "password";
//             eyeIcon.classList.replace("bx-show", "bx-hide");
//         })
//
//     })
// })

// links.forEach(link => {
//     link.addEventListener("click", e => {
//         e.preventDefault(); //preventing form submit
//         forms.classList.toggle("show-signup");
//     })
// })