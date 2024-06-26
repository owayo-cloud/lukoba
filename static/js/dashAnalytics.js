document.addEventListener('DOMContentLoaded', function() {
    // Example data for insights
    document.getElementById('tickets-sold').textContent = '1,074';
    document.getElementById('visitors').textContent = '3,944';
    document.getElementById('conversion-rate').textContent = '12.4%';
    document.getElementById('revenue').textContent = '$6,742';

    // Tickets Sold Chart
    const ticketsSoldCtx = document.getElementById('ticketsSoldChart').getContext('2d');
    new Chart(ticketsSoldCtx, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'Tickets Sold',
                data: [100, 200, 150, 300, 250, 350],
                backgroundColor: 'rgba(77, 198, 214, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
                label: 'Revenue',
                data: [1000, 2000, 1500, 3000, 2500, 3500],
                backgroundColor: 'rgba(54, 162, 235, 1)',
                borderColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
