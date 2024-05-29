document.addEventListener('DOMContentLoaded', () => {
    // Hide login form by default
    document.getElementById('lFormC').style.display = 'none';

    const registerForm = document.getElementById('rForm');
    const loginForm = document.getElementById('lForm');

    registerForm.addEventListener('submit', handleRegistration);
    loginForm.addEventListener('submit', handleLogin);

    window.redirectToIndex = function() {
        window.location.href = "index.html";
    }

    window.toggleForm = function(formType) {
        const rFormC = document.getElementById('rFormC');
        const lFormC = document.getElementById('lFormC');

        if (formType === 'login') {
            rFormC.style.display = 'none';
            lFormC.style.display = 'block';
        } else if (formType === 'registration') {
            rFormC.style.display = 'block';
            lFormC.style.display = 'none';
        } else if (formType === 'forgot') {
            alert('Forgot Password functionality is not implemented yet.');
        }
    }

    function postData(url, data) {
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

    function handleRegistration(event) {
        event.preventDefault();

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !email || !password) {
            alert('Please fill in all fields.');
            return;
        }

        if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
            alert('Password must be at least 8 characters long and contain at least 1 capital letter and a number.');
            return;
        } else {
            alert('Registration successful');
        }

        postData('http://localhost:8000/user/register', { username, email, password })
        .then(response => {
            if (response.status === 'success') {
                document.cookie = `user_email=${email}; path=/;`;
                alert('Registration Successful:' + response.message);
                window.location.reload();
            } else {
                alert('Registration failed:' + response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during registration.');
        });
    }

    function handleLogin(event) {
        event.preventDefault();

        const email = document.getElementById('lEmail').value.trim();
        const password = document.getElementById('lPass').value.trim();

        postData('http://localhost:8000/user/login', { email, password })
        .then(response => {
            if (response.status === 'success') {
                document.cookie = `user_email=${email}; path=/;`;
                alert(response.message);
                window.location.reload();
            } else {
                alert(response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during login.');
        });
    }
});
