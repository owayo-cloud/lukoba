let loginBtn = document.getElementById("loginBtn");
let registerBtn = document.getElementById("registerBtn");
let nameField = document.getElementById("nameField");
let title = document.getElementById("title");

loginBtn.onclick = function(){
    
    nameField.style.maxHeight = "0";
    title.innerHTML = "Login"
    registerBtn.classList.add("disable");
    loginBtn.classList.remove("disable");
}
registerBtn.onclick = function(){
    
    nameField.style.maxHeight = "60px";
    title.innerHTML = "Register"
    loginBtn.classList.add("disable");
    registerBtn.classList.remove("disable");
}
document.addEventListener("DOMContentLoaded", function() {
    // Select the signup form and relevant input fields
    const signupForm = document.getElementById('signupForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('signupEmail');
    const passwordInput = document.getElementById('signupPassword');

    signupForm.addEventListener('submit', function(event) { // Attaches an event listener to the form submission event
        event.preventDefault(); // Prevents the default form submission

        // Validate name, email, and password
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (!name || !email || !password) {
            alert('Please fill in all fields.'); // Display error message if any field is empty
            return;
        }

        // Check if password meets criteria
        if (password.length < 8) {
            // Display error message if password length is less than 8
            alert('Password must be at least 8 characters long.');
            return;
        }

        if (!/[A-Z]/.test(password)) {
            // Display error message if password doesn't contain at least 1 capital letter
            alert('Password must contain at least 1 capital letter.');
            return;
        }

        if (!/\d/.test(password)) {
            // Display different error message if password doesn't contain at least 1 number
            alert('Password must contain at least 1 number.');
            return;
        }
        
        // Additional validation logic (e.g., checking email format, password strength) can be added here
        // If validation passes, you can proceed with signing up (for demonstration, just showing an alert)
        alert('Registration successfully!');
        // Here, you can add code to redirect the user to a dashboard or perform other actions after signing up
    });
});
