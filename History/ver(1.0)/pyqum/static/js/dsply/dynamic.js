function myPlot(canvas, datax, datay) {
    
//    document.getElementById(output).innerHTML = "Y1-Data: " + datay.slice(0,6);
    var ctx = document.getElementById(canvas).getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: datax,
            datasets: [{
                fill: false,
                label: "CN",
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: datay      


            }]
        },

        // Configuration options go here
        options: {animation: false}
    });
}