// get DOM
let nextDom = document.getElementById('next');
let prevDom = document.getElementById('prev');
let extras = document.getElementById('extras');
let bkNow = document.getElementById('bkNow'); 
let carouselDom = document.querySelector('.carousel');
let SliderDom = carouselDom.querySelector('.carousel .list');
let thumbnailBorderDom = document.querySelector('.carousel .thumbnail');
let thumbnailItemsDom = thumbnailBorderDom.querySelectorAll('.item');
let timeDom = document.querySelector('.carousel .time');

// redirect functions

function redirectToLogin() {
    window.location.href = "login.html";
}
function redirectToHome() {
    window.location.href = "home.html";
}

thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
let timeRunning = 3000;
let timeAutoNext = 5000;

extras.onclick = function(){
    window.open('shows.html', '_self');
}
document.addEventListener('DOMContentLoaded', function(){
    const bkNow = document.getElementById('bkNow');
    
    bkNow.onclick = function(){
        // Get the movie title dynamically from the content
        let movieTitle = document.getElementById('movieTitle').innerText;
        redirectToBooking('movieTitle'); 
    }

    function redirectToBooking(movieTitle) {
        window.location.href = `booking.html?movie=${encodeURIComponent(movieTitle)}`;
    }
});

document.addEventListener('DOMContentLoaded', () =>{
    //retrieve user info from local storage
    const user = JSON.parse(localStorage.getItem('user'));
    const usernameElement = document.getElementById('username');
    const welcomeMessageElement = document.getElementById('welcomeMessage');

    if (user){
        document.getElementById('user-controls').style.display = 'block';
    } else{
        // If no user is logged in, show the login button
        document.getElementById('sign').style.display = 'block';
    }
});

document.getElementById('sign').addEventListener('click', redirectToLogin);

function redirectToLogin(){
    window.location.href = "login.html"
}

nextDom.onclick = function(){
    showSlider('next');    
}
prevDom.onclick = function(){
    showSlider('prev');    
}
let runTimeOut;
let runNextAuto = setTimeout(() => {
    next.click();
}, timeAutoNext)
function showSlider(type){
    let  SliderItemsDom = SliderDom.querySelectorAll('.carousel .list .item');
    let thumbnailItemsDom = document.querySelectorAll('.carousel .thumbnail .item');
    
    if(type === 'next'){
        SliderDom.appendChild(SliderItemsDom[0]);
        thumbnailBorderDom.appendChild(thumbnailItemsDom[0]);
        carouselDom.classList.add('next');
    }else{
        SliderDom.prepend(SliderItemsDom[SliderItemsDom.length - 1]);
        thumbnailBorderDom.prepend(thumbnailItemsDom[thumbnailItemsDom.length - 1]);
        carouselDom.classList.add('prev');
    }
    clearTimeout(runTimeOut);
    runTimeOut = setTimeout(() => {
        carouselDom.classList.remove('next');
        carouselDom.classList.remove('prev');
    }, timeRunning);

    clearTimeout(runNextAuto);
    runNextAuto = setTimeout(() => {
        next.click();
    }, timeAutoNext)
}
//TOGGLE

const ball = document.querySelector(".toggle-ball");
const items = document.querySelectorAll(
  ".container,.movie-list-title,.navbar-container,.sidebar,.left-menu-icon,.toggle"
);

ball.addEventListener("click", () => {
  items.forEach((item) => {
    item.classList.toggle("active");
  });
  ball.classList.toggle("active");
});