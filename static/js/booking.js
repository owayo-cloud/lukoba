function redirectToHome() {
    window.location.href = "index.html";
}
function redirectToLogin(){
  window.location.href = "login.html";
}
//Generate seat checkboxes
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
//Add event listeners to seat checkboxes
let tickets = seats.querySelectorAll("input");
tickets.forEach((ticket) => {
  ticket.addEventListener("change", () => {
    let amount = document.querySelector(".amount").innerHTML;
    let count = document.querySelector(".count").innerHTML;
    amount = Number(amount);
    count = Number(count);

    if (ticket.checked) {
      count += 1;
      amount += 200;
    } else {
      count -= 1;
      amount -= 200;
    }
    document.querySelector(".amount").innerHTML = amount;
    document.querySelector(".count").innerHTML = count;
  });
});