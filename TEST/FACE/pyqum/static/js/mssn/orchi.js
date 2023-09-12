//when page is loading:
$(document).ready(function(){
    $('div.orchicontent').hide();
    window.orchi_TASK = "";
    return false;
});

// RETURN to Sample selection page:
$('input.orchi.loaded#sample-name').on('click', function() {
    window.location.href='/auth/user';
    return false;
});

// Get TASK name:
$('button.orchi.access.QPX').on('click', function() { 
    orchi_TASK = this.id;
    console.log("Clicking on " + orchi_TASK);
 });

// Benchmark on click > Loading measurement data into Benchmark:
$('#orchi-to-benchmark').click( function(){
    $.ajaxSettings.async = false;

    // listimes_singleqb(); accessdata_singleqb();
    // $.getJSON(mssnencrpytonian() + '/mssn/QPX/access', { wmoment: wmoment }, function (data) { console.log("JOBID: " + JSON.stringify(data.JOBID) ); console.log(data); });

    let quantificationType = ["qfactor_estimation"];
    $.getJSON( '/benchmark/benchmark_getMeasurement', 
    { measurementType: orchi_TASK, quantificationType: JSON.stringify(quantificationType) }, 
        function () {
    }); 

    window.open("/benchmark");
    $.ajaxSettings.async = true;
    return false;
    }
);
 
