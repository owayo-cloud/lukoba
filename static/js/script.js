// get DOM
let nextDom = document.getElementById('next');
let prevDom = document.getElementById('prev');
let carouselDom = document.querySelector('.carousel');
let SliderDom = carouselDom.querySelector('.carousel .list');
let thumbnailBorderDom = document.querySelector('.carousel .thumbnail');
let thumbnailItemsDom = thumbnailBorderDom.querySelectorAll('.item');
let timeDom = document.querySelector('.carousel .time');

let timeRunning = 3000;
let timeAutoNext = 5000;

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
    let SliderItemsDom = SliderDom.querySelectorAll('.carousel .list .item');
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

    // Update active class
    updateActiveClass();

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

// Add click event listeners to thumbnails
thumbnailItemsDom.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', () => {
        showSpecificSlider(index);
    });
});

function showSpecificSlider(index) {
    let SliderItemsDom = Array.from(SliderDom.querySelectorAll('.carousel .list .item'));
    
    // Reset the carousel to display the clicked item
    while (SliderDom.firstChild) {
        SliderDom.removeChild(SliderDom.firstChild);
    }
    for (let i = index; i < SliderItemsDom.length; i++) {
        SliderDom.appendChild(SliderItemsDom[i]);
    }
    for (let i = 0; i < index; i++) {
        SliderDom.appendChild(SliderItemsDom[i]);
    }
    
    let thumbnailItemsDom = Array.from(thumbnailBorderDom.querySelectorAll('.carousel .thumbnail .item'));
    
    // Reset the thumbnails to display the clicked thumbnail as active
    while (thumbnailBorderDom.firstChild) {
        thumbnailBorderDom.removeChild(thumbnailBorderDom.firstChild);
    }
    for (let i = index; i < thumbnailItemsDom.length; i++) {
        thumbnailBorderDom.appendChild(thumbnailItemsDom[i]);
    }
    for (let i = 0; i < index; i++) {
        thumbnailBorderDom.appendChild(thumbnailItemsDom[i]);
    }

    // Update active class
    updateActiveClass();

    clearTimeout(runTimeOut);
    runTimeOut = setTimeout(() => {
        carouselDom.classList.remove('next');
        carouselDom.classList.remove('prev');
    }, timeRunning);

    clearTimeout(runNextAuto);
    runNextAuto = setTimeout(() => {
        next.click();
    }, timeAutoNext);
}

// Update active class for the carousel and thumbnails
function updateActiveClass() {
    let SliderItemsDom = SliderDom.querySelectorAll('.carousel .list .item');
    let thumbnailItemsDom = thumbnailBorderDom.querySelectorAll('.carousel .thumbnail .item');

    SliderItemsDom.forEach(item => item.classList.remove('active'));
    thumbnailItemsDom.forEach(item => item.classList.remove('active'));

    SliderItemsDom[0].classList.add('active');
    thumbnailItemsDom[0].classList.add('active');
}

// TOGGLE
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
