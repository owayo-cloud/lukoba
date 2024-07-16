//Generate seats
let seats = document.querySelector(".all-seats");
let rows = "JIHGFEDCBA"; // Define 10 rows for simplicity
let cols = 6; // Define 6 columns

for (let row = 0; row < rows.length; row++) {
    for (let col = 1; col <= cols; col++) {
      let seatLabel = rows[row] + col;
      let randint = Math.floor(Math.random() * 2);
      let booked = randint === 1 ? "booked" : "";
      seats.insertAdjacentHTML(
        "beforeend",
        '<input type="checkbox" name="tickets" id="' + seatLabel + '" />' +
        '<label for="' + seatLabel + '" class="seat ' + booked + '">' + seatLabel + '</label>'
      );
    }
  }