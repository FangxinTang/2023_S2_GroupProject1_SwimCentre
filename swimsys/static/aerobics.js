// static/aerobics.js





document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('barChart').getContext('2d');
    
    console.log('hello!!');


    var myChart = new Chart(ctx, {
        type: 'bar', 
        data: {
            labels: courseLabels,
            datasets: [{
                label: 'Attendance Counts',
                data: aerobicsData,
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
            },
            // tooltip: {
            //     callbacks: {
            //         label: function(context) {

            //             console.log('hello!!');

            //             var courseTooltipData = courseInfo[context.dataIndex];
            //             return Object.keys(courseTooltipData)
            //                 .map(key => key + ': ' + courseTooltipData[key])
            //                 .join('\n');
            //         }
            //     }
            // }
        },
    });
})
