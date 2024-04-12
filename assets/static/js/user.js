let loginBtn = document.getElementById("loginBtn");
let registerBtn = document.getElementById("registerBtn");
let nameField = document.getElementById("nameField");
let title = document.getElementById("title");

loginBtn.onclick = function(){
    nameField.style.maxHeight = '0';
    title.innerHTML = 'Login';
    registerBtn.classList.add('disable');
    loginBtn.classList.remove('disable');
}
registerBtn.onclick = function(){
    nameField.style.maxHeight = '60px';
    title.innerHTML = 'Sign Up'
    loginBtn.classList.add('disable');
    registerBtn.classList.remove('disable');
}

document.addEventListener('DOMContentLoaded', function(){
    const signupForm = document.getElementById('signupForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('signupEmail');
    const passwordInput = document.getElementById('signupPassword');

    //Function for sending HTTP POST request
    function postData(url, data) {
        //validate URL
        if (!url || typeof url !== 'string') {
            return Promise.reject(new Error('Invalid URL provided'));
        }
    
        // Validate data
        if (!data || typeof data !== 'object' || Object.keys(data).length === 0) {
            return Promise.reject(new Error('Invalid data provided'));
        }
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .catch(error => {
            console.error('Error:', error);
            throw new Error('Failed to send POST request');
        });
    }

    //Function for handling registration
    function handleRegistration(event) {
        event.preventDefault();

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Validate inputs
        if (!name || !email || !password) {
            alert('Please fill in all fields.');
            return;
        }

        if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
            alert('Password must be at least 8 characters long and contain at least 1 capital letter and a number.');
            return;
        }
        else{
            alert('Registration successful');
        }

        //sending registration back to backend
        postData('http://localhost:8000/user/register', { username: name, email: email, password: password })
        .then(response => {
            if (response && response.status === 'success') {
                alert('Registration Successful:' + response.message);
            } else {
                alert('Registration failed:' + response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during registration.');
        });
    }
    //Function for handling login
    function handleLogin(event){
        event.preventDefault()

        const email = emailInput.value.trim(); // Assuming email is used for login
        const password = passwordInput.value.trim();

        //sending login data to backend
        postData('http://localhost:8000/user/login', {email: email, password:password})
        .then(response => {
            if(response.status === 'success'){
                alert(response.message);

                //either redirect user to dashboard or perform other actions
            } else{
                alert(response.message);
            }
        });
    }

    // event listeners for register and login buttons
    registerBtn.addEventListener('click', handleRegistration);
    loginBtn.addEventListener('click', handleLogin);
});
