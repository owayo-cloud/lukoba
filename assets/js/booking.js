function redirectToHome() {
    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", function(){
    // Get Movie title from URL
    const urlParams  =new URLSearchParams(window.location.search);
    const movieTitle = urlParams.get('movie');
    if (movieTitle){
        document.getElementById('movieTitle').textContent = movieTitle
    }
})
    //Generate seat checkboxes
    let seats = document.querySelector(".all-seats");
      for (var i = 0; i < 60; i++) {
        let randint = Math.floor(Math.random() * 2);
        let booked = randint === 1 ? "booked" : "";
        seats.insertAdjacentHTML(
          "beforeend",
          '<input type="checkbox" name="tickets" id="s' +
            (i + 2) +
            '" /><label for="s' +
            (i + 2) +
            '" class="seat ' +
            booked +
            '"></label>'
        );
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
      // form submission handler
      document.querySelector(".price button").addEventListener("click", function(){
        alert('Booking successful!');
        // Here you can add the logic to save the booking to the database
      });