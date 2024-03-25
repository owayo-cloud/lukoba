document.addEventListener("DOMContentLoaded", function() {
    const seats = document.querySelectorAll('.seat');
    const userDetailsForm = document.getElementById('user_details_form');
    const bookButton = document.getElementById('book-btn');

    let selectedSeats = [];
    let selectedSeatType = 'regular';

    // Event listener for user details form submission
    userDetailsForm.addEventListener('submit', function(event) {
        event.preventDefault(); //prevents form from submitting automatically
        // Code to capture user details and date selection
        // Get user details and date selection
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const date = document.getElementById('date').value;

        // Do something with the captured user details and date selection
        console.log('Name:', name);
        console.log('Email:', email);
        console.log('Selected Date:', date);

        // You can also perform validation or other actions here
        // Enable book button after user details are filled
        bookButton.disabled = false;
    });

    // Event listener for seat selection
    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            if (!seat.classList.contains('booked')) {
                seat.classList.toggle('selected');
                const seatType = seat.classList.contains('vip') ? 'vip' : 'regular';
                if (seat.classList.contains('selected')) {
                    selectedSeats.push({ seat: seat.dataset.seat, type: seatType });
                } else {
                    selectedSeats = selectedSeats.filter(s => s.seat !== seat.dataset.seat);
                }
                updateSelectedSeats();
            }
        });
    });

    // Event listener for seat type selection
    document.querySelectorAll('input[name="seat-type"]').forEach(input => {
        input.addEventListener('change', () => {
            selectedSeatType = input.value;
        });
    });

    // Function to update selected seats, user details, and total amount
    function updateSelectedSeats() {
        const userName = document.getElementById('name').value;
        const userEmail = document.getElementById('email').value;
        const selectedSeatsText = selectedSeats.length > 0 ? selectedSeats.map(s => s.seat).join(', ') : 'None';
        document.getElementById('selected-seats').textContent = selectedSeatsText;
        document.getElementById('user-details').textContent = `User: ${userName} (${userEmail})`;
        // Calculate total amount based on the selected seats and seat type
        const totalPrice = selectedSeats.reduce((total, seat) => {
            return total + (seat.type === 'vip' ? 15 : 10); // Adjust prices as needed
        }, 0);
        document.getElementById('total-amount').textContent = `$${totalPrice.toFixed(2)}`;
        // Enable book button if at least one seat is selected
        bookButton.disabled = selectedSeats.length === 0;
    }

    // Function to mark seats as booked
    function markSeatsAsBooked(bookedSeats) {
        seats.forEach(seat => {
            if (bookedSeats.includes(seat.dataset.seat)) {
                seat.classList.add('booked');
            }
        });
    }

    // Example: Call markSeatsAsBooked with an array of booked seat IDs
    const bookedSeats = ['A1', 'B3', 'C2']; // Replace with actual booked seat IDs
    markSeatsAsBooked(bookedSeats);
});
