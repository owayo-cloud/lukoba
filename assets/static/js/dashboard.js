const sideLinks = document.querySelectorAll('.sidebar .sideMenu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});
const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});
const searchBtn = document.querySelector('.content nav form .form_input button');
const searchBtnIcon = document.querySelector('.content nav form .form_input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});
window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});
const toggler = document.getElementById('theme-toggle');
toggler.addEventListener('change', function () {
    console.log('checkbox changed');
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});
//Ajax requests for login
const loginBtn = document.querySelector('#login-btn');
loginBtn.addEventListener('click', () =>{
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    //performing ajax requests
    $.ajax({
        url: "http://localhost:8000/login",
        data: JSON.stringify({ email: email, password: password }),
        contentType: "application/json",
        success: function(response) {
            console.log(response);
            // Handle successful login response here
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
            // Handle login error here
        }
    })
});

// AJAX request for registration
const registerBtn = document.querySelector('#register-btn');
registerBtn.addEventListener('click', () => {
    const username = document.querySelector('#username').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const profilePicture = document.querySelector('#profile-picture').value;

    // Perform AJAX request
    $.ajax({
        type: "POST",
        url: "http://localhost:8000/register",
        data: JSON.stringify({ username: username, email: email, password: password, profilePicture: profilePicture }),
        contentType: "application/json",
        success: function(response) {
            console.log(response);
            // Handle successful registration response here
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
            // Handle registration error here
        }
    });
});