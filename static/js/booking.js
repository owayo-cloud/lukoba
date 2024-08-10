// Generate seats
let seats = document.querySelector(".all-seats");
let rows = "EDCBA"; // Define 5 rows
let cols = 5; // Define 5 columns
let seatPrice = 1; // Define a constant price for each seat
let totalAmount=0
// Function to fetch booked seats
async function fetchBookedSeats() {
    return JSON.parse(bookings?.replace(/'/g, '"'));
}

// Function to generate seats
async function generateSeats() {
    let bookedSeats = await fetchBookedSeats();

    for (let row = 0; row < rows.length; row++) {
        for (let col = 1; col <= cols; col++) {
            let seatLabel = rows[row] + col;
            let booked = bookedSeats?.find((seat) => seat === seatLabel) ? "booked" : "";
            seats.insertAdjacentHTML(
                "beforeend",
                `<div class="seat-wrapper">
                    <input type="checkbox" name="tickets" id="${seatLabel}" ${booked ? "disabled" : ""}/>
                    <label for="${seatLabel}" class="seat ${booked}">${seatLabel}</label>
                    <span class="seat-price">${seatPrice}</span>
                </div>`
            );
        }
    }

    // Add event listeners to toggle 'selected' class
    let seatLabels = document.querySelectorAll(".seat:not(.booked)");
    seatLabels.forEach((label) => {
        label.addEventListener("click", function () {
            if (!label.classList.contains("booked")) {
                label.classList.toggle("selected");
                let checkbox = document.getElementById(label.getAttribute("for"));
                checkbox.checked = !checkbox.checked;
                document.getElementById("seat_number").value = checkbox.checked ? label.textContent : '';

                updateTotalAmount();
            }
        });
    });
}

// Function to update total amount
function updateTotalAmount() {
    let selectedSeats = document.querySelectorAll(".seat.selected");
    totalAmount = selectedSeats.length * seatPrice;
    document.getElementById("total_amount").textContent = totalAmount;
    document.getElementById("seat_price").value = totalAmount;
}

// Generate seats on page load
generateSeats();

// handle btn click
document.querySelector("#book-button").addEventListener("click", function () {
    // get seats
    let selectedSeats = document.querySelectorAll(".selected");
    let selectedSeatLabels = [];
    selectedSeats.forEach((seat) => {
        selectedSeatLabels.push(seat.textContent);
    });
    // get show time from input named showtime
    let showTime = document.querySelector('input[name="showtime"]')?.value;
    // get movie id
    let movieId = document.querySelector('input[name="movieId"]')?.value;
    let movieImdb = document.querySelector('input[name="movieImdb"]')?.value;
    // validate data
    if (selectedSeatLabels.length === 0 || !showTime || !movieId) {
        alert("Please select seats and show time");
        return;
    }
    // send data to server on the same url
    submitBookingForm(movieImdb, movieId, selectedSeatLabels, showTime);
});

function submitBookingForm(imdb, movie, seats, showtime) {
    // Create a form element
    const form = document.createElement("form");
    form.method = "POST";
    form.action = window.location.href.split('?')[0]; // Assuming this is the correct endpoint URL

    // Create and append input fields
    const fields = {
        imdb: imdb,
        movie: movie,
        seats: seats,
        showtime: showtime,
    }; 

    fields['phone_number'] = document.getElementById('phone_number').value;
    fields['amount'] = totalAmount

    for (const [name, value] of Object.entries(fields)) {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
    }

    // Append the form to the body and submit it
    document.body.appendChild(form);
    form.submit();

    // Remove the form from the document
    document.body.removeChild(form);
}

document.querySelector("input[name='showtime_sel']").addEventListener("click", function (e) {
    // pass as query to url
    const url = new URL(window.location.href);
    url.searchParams.set('s', e.target.value);
    window.location.href = url.toString();
});

