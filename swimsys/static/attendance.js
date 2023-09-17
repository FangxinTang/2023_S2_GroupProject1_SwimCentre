// static/attendance.js

document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('barChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar', // Change the chart type to 'bar'
        data: {
            labels: activityLabels,
            datasets: [{
                label: 'Attendance Counts',
                data: attendanceData,
                backgroundColor: 'rgb(75, 192, 192)', // Set the color for the bars
                borderWidth: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true // To stack bars on the x-axis if desired
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1, // Set the step size to 1
                        precision: 0
                    }
                }
            }
        }
    });
});
