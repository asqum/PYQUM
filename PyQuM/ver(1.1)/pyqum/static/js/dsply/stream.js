function SChart(canvas, data) {
    var ctx = document.getElementById(canvas).getContext('2d');
    var scatterChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Scatter Dataset',
            pointBackgroundColor: 'rgb(202, 25, 75)',
            pointRadius: 3.7,
            data: data
        }]
    },
    options: {
        animation: {
            duration: 0, // general animation time
        },
        hover: {
            animationDuration: 0, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
//        animation: false,
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }]
        }
    }
});
    
}