function redirectToHome() {
    window.location.href = "index.html";
}
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const movie = urlParams.get('movie');

    //retrieve modal and form elements
    const modal = document.getElementById("bModal");
    const closeModal = document.getElementsByClassName("close")[0];
    const bForm = document.getElementById('bForm');

    // If movie parameter exists, set it as the value of the movie input field and display the modal
    if (movie) {
        const movieSelect = document.getElementById('movie');
        movieSelect.value = movie;

        // ensure movie is in the drop down menu, if not add it
        let optionExists = false;
        for (let i = 0; i < movieSelect.options.length; i++) {
            if (movieSelect.options[i].value === movie) {
                optionExists = true;
                break;
            }
        }
        if (!optionExists) {
            let newOption = document.createElement("option");
            newOption.value = movie;
            newOption.text = movie;
            movieSelect.add(newOption);
            movieSelect.value = movie;
        }
        
        modal.style.display = "block";
    }

    // Add event listener to close the modal when clicking on the close button
    if (closeModal) {
        closeModal.onclick = function() {
            modal.style.display = "none";
        }
    }

    // Add event listener to close the modal when clicking outside the modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    
    // Add event listener to the form for handling booking submission
    if (bForm) {
        bForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Retrieve form data
            const date = document.getElementById('date').value;
            const time = document.getElementById('time').value;
            const seats = document.getElementById('seats').value;
            
            // Now you can submit the form data or perform any other actions as needed
            alert('Booking Confirmed!');
            modal.style.display = "none";
        });
    }
});
