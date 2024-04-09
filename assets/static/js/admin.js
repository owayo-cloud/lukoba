function toggleForm(formType) {
    const registrationFormContainer = document.getElementById('registrationFormContainer');
    const loginFormContainer = document.getElementById('loginFormContainer');

    if (formType === 'login') {
        registrationFormContainer.style.display = 'none';
        loginFormContainer.style.display = 'block';
    } else if (formType === 'registration') {
        registrationFormContainer.style.display = 'block';
        loginFormContainer.style.display = 'none';
    } else if (formType === 'forgot') {
        // Handle forgot password functionality here
        alert('Forgot Password functionality is not implemented yet.');
    }
}

// Hide login form by default
document.getElementById('loginFormContainer').style.display = 'none';

document.getElementById('registrationForm').addEventListener('submit', function(event){
    //prevent the default form submission
    event.preventDefault();

    //validate the form data
    let username = document.getElementById('username').value.trim();
    let email = document.getElementById('email').value.trim();
    let password = document.getElementById('password').value.trim();
    let profilePicture = document.getElementById('profilePicture').value.trim();

    //perform validation checks
    if (username === '' || email === '' || password === '' || profilePicture === '') {
        alert('Please fill in all the fields');
        return;
    }
    if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
        alert('Password must be at least 8 characters long and contain at least 1 capital letter and a number.');
        return;
    }

    // Call the handleRegistration function
    handleRegistration(username, email, password, profilePicture);
});

function handleRegistration(username, email, password, profilePicture) {
    const data = { username, email, password, profilePicture };

    // Function for sending HTTP POST request
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

    // Sending registration back to backend
    postData('http://localhost:8000/register', data)
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
