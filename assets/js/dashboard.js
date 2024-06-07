document.addEventListener('DOMContentLoaded', function(){
    const dashboardLink = document.getElementById('dashboard-link');
    const moviesLink = document.getElementById('movies-link');
    const analyticsLink = document.getElementById('analytics-link');
    const bookingsLink = document.getElementById('bookings-link');
    const usersLink = document.getElementById('users-link');
    const settingsLink = document.getElementById('settings-link');
    const logoutLink = document.getElementById('logout-link');

    // Event listeners for sidebar navigation
    dashboardLink.addEventListener('click', loadDashboard);
    moviesLink.addEventListener('click', loadMovies);
    analyticsLink.addEventListener('click', loadAnalytics);
    bookingsLink.addEventListener('click', loadBookings);
    usersLink.addEventListener('click', loadUsers);
    settingsLink.addEventListener('click', loadSettings);
    logoutLink.addEventListener('click', logout);

    //function to get cookie value by name
    function getCookie(name){
        const value = '; ${document.cookie}';
        const parts = value.split('; ${name}=');
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    //check if user logged in is an admin
    const userEmail = getCookie('user_email');

    if (!userEmail){
        // if no user email is found in cookies, redirect to login page
        window.location.href = 'login.html';
    }else{
        //verify the user is an admin
        fetch(`http://localhost:8000/user/details?email=${userEmail}`)
        .then(response => response.json())
        .then(data =>{
            if(data.is_admin){
                //display the admin dashboard
                document.getElementById('dashboard-section').style.display = 'block';
                document.getElementById('admin-name').innerText = data.username;
                //Fetch and update metrics and recent bookings
                updateMetrics();
                updateRecentBookings();
            }else{
                //if the user is not an admin, redirect to the login page
                window.location.href  = 'login.html';
            }
        })
        .catch(error =>{
            console.error('Error:', error);
            alert('An error occurred while verifying the user.');
            window.location.href = 'login.html';
        });
    }

    function loadDashboard(){

    }

    function loadMovies() {
        // Code to load movies data
    }

    function loadAnalytics() {
        // Code to load analytics data
    }

    function loadBookings() {
        // Code to load bookings data
    }

    function loadUsers() {
        // Code to load users data
    }

    function loadSettings() {
        // Code to load settings data
    }

    function logout(){
        //code for logout
        fetch('/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response =>{
            if(response.ok){
                // Clear cookies and redirect to login
                document.cookie = 'user_email=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                window.location.href = '/login.html';
            }
        }).catch(error =>{
            console.error('Error:', error);
            alert('An error occurred during logout.');
        });
    }
    document.getElementById('logout-link').addEventListener('click', logout);

    // Fetch and update dashboard metrics
    function updateMetrics() {
        fetch('/api/dashboard-metrics')
            .then(response => response.json())
            .then(data => {
                document.getElementById('tickets-sold').innerText = data.ticketsSold;
                document.getElementById('visitors').innerText = data.visitors;
                document.getElementById('searches').innerText = data.searches;
                document.getElementById('revenue').innerText = data.revenue;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching metrics.');
            });
    }

    //fetch update recent bookings
    function updateRecentBookings(){
        fetch('/api/recent-bookings')
            .then(response => response.json())
            .then(data => {
                const bookingsTable = document.getElementById('recent-bookings');
                bookingsTable.innerHTML = '';
                data.bookings.forEach(booking => {
                    bookingsTable.innerHTML += `
                        <tr>
                            <td><p>${booking.user}</p></td>
                            <td>${booking.movie}</td>
                            <td>${booking.bookingDate}</td>
                            <td>${booking.showtime}</td>
                            <td><span class="status ${booking.status.toLowerCase()}">${booking.status}</span></td>
                        </tr>
                    `;
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching recent bookings.');
            });
    }
});
// Handle sidebar active link
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