// Generate seats
let seats = document.querySelector(".all-seats");
let rows = "EDCBA"; // Define 5 rows
let cols = 5; // Define 5 columns
let movieId = "123"; // Replace with actual movie ID

// Function to fetch booked seats
async function fetchBookedSeats(movieId) {
    try {
        let response = await fetch(`/seats?movie_id=${movieId}`);
        let data = await response.json();
        return data.booked || [];
    } catch (error) {
        console.error('Error fetching booked seats:', error);
        return [];
    }
}

// Function to generate seats
async function generateSeats() {
    let bookedSeats = await fetchBookedSeats(movieId);
    let bookedSeatsSet = new Set(bookedSeats);

    for (let row = 0; row < rows.length; row++) {
        for (let col = 1; col <= cols; col++) {
            let seatLabel = rows[row] + col;
            let booked = bookedSeatsSet.has(seatLabel) ? "booked" : "";
            seats.insertAdjacentHTML(
                "beforeend",
                '<div class="seat-wrapper">' +
                '<input type="checkbox" name="tickets" id="' + seatLabel + '" ' + (booked ? 'disabled' : '') + '/>' +
                '<label for="' + seatLabel + '" class="seat ' + booked + '">' + seatLabel + '</label>' +
                '</div>'
            );
        }
    }

    // Add event listeners to toggle 'selected' class
    let seatLabels = document.querySelectorAll(".seat:not(.booked)");
    seatLabels.forEach(label => {
        label.addEventListener("click", function () {
            if (!label.classList.contains("booked")) {
                label.classList.toggle("selected");
                let checkbox = document.getElementById(label.getAttribute("for"));
                checkbox.checked = !checkbox.checked;
            }
        });
    });
}

// Generate seats on page load
generateSeats();
