function redirectToIndex() {
    window.location.href = "index.html";
}
function redirectToHome() {
    window.location.href = "home.html";
}

//carousel item data array
const carouselData = [
    {
        imageSrc: '../static/assets/images/IT.jpg',
        author: 'STEPHEN KING',
        title: 'IT',
        genre: 'Horror, Drama, Thriller',
        description: '"It" (2017) is a horror film directed by Andy Muschietti, based on the 1986 novel of the same name by Stephen King. The story revolves around a group of children in the fictional town of Derry, Maine, who are terrorized by a shape-shifting entity that primarily takes the form of a malevolent clown named Pennywise. The entity preys on the children\'s deepest fears, often manifesting as their worst nightmares. As the children confront their fears and uncover the truth about the entity, they form a bond and make a pact to defeat "It" once and for all. The film explores themes of friendship, bravery, and the loss of innocence, as the children face both the supernatural horrors of Pennywise and the real-world challenges of growing up in a troubled town.'
    },
    //for extra items
];

const thumbnailData = [
    {
        imageSrc: '../static/assets/images/IT.jpg',
        title: 'Stephen King IT',
        description: 'IT'
    }
    //for extra items
];

//function to generate carousel items dynamically
function generateCarouselItem(data){
    const {imageSrc, author, title, genre, description} = data;

    const itemDiv = document.createElement('div');
    itemDiv.classList.add('item');

    const img = document.createElement('img');
    img.src = imageSrc;
    img.alt = title;
    itemDiv.appendChild(img);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');

    const authorDIv = document.createElement('div');
    authorDIv.classList.add('author');
    authorDIv.textContent = author;
    contentDiv.appendChild(authorDIv);

    const titleDiv = document.createElement('div');
    titleDiv.classList.add('title');
    titleDiv.textContent = title;
    contentDiv.appendChild(titleDiv);

    const genreDiv = document.createElement('div');
    genreDiv.classList.add('genre');
    genreDiv.textContent = genre;
    contentDiv.appendChild(genreDiv);

    const desDiv = document.createElement('div');
    desDiv.classList.add('des');
    desDiv.textContent = description;
    contentDiv.appendChild(desDiv);

    const buttonsDiv = document.createElement('div');
    buttonsDiv.classList.add('buttons');

    const seeMoreBtn = document.createElement('button');
    seeMoreBtn.id = 'extras';
    seeMoreBtn.textContent = 'SEE MORE';
    buttonsDiv.appendChild(seeMoreBtn);

    const bookNowBtn = document.createElement('button');
    bookNowBtn.id = 'bNow';
    bookNowBtn.textContent = 'BOOK NOW';
    buttonsDiv.appendChild(bookNowBtn);

    contentDiv.appendChild(buttonsDiv);

    itemDiv.appendChild(contentDiv);

    return itemDiv;
}

function generateThumbnailItem(data){
    const{ imageSrc, title, description} = data;

    const itemDiv = document.createElement('div');
    itemDiv.classList.add('item');

    const img = document.createElement('img');
    img.src = imageSrc;
    img.alt = title;
    itemDiv.appendChild(img);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');

    const titleDiv = document.createElement('div');
    titleDiv.classList.add('title');
    titleDiv.textContent = title;
    contentDiv.appendChild(titleDiv);

    const descriptionDiv = document.createElement('div');
    descriptionDiv.classList.add('description');
    descriptionDiv.textContent = description;
    contentDiv.appendChild(descriptionDiv);

    itemDiv.appendChild(contentDiv);

    return itemDiv;
}

//getting carousel&thumbnail list container
const carouselList = document.querySelector('.carousel .list');
const thumbnailList = document.querySelector('.thumbnail');

// Generate and append thumbnail & carousel items
thumbnailData.forEach(data => {
    const thumbnailItem = generateThumbnailItem(data);
    thumbnailList.appendChild(thumbnailItem);
});

carouselData.forEach(data => {
    const carouselItem = generateCarouselItem(data);
    carouselList.appendChild(carouselItem);
});