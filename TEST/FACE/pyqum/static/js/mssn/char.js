//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();
    window.char_TASK = "";
    return false;
});

// RETURN to Sample selection page:
$('input.char.loaded#sample-name').on('click', function() {
    window.location.href='/auth/user';
    return false;
});

// Get TASK name:
$('button.char.access.fresp').on('click', function() { char_TASK = 'fresp' });
$('button.char.access.cwsweep').on('click', function() { char_TASK = 'cwsweep' });
$('button.char.access.sqepulse').on('click', function() { char_TASK = 'sqepulse' });

// Benchmark on click > Loading measurement data into Benchmark:
$('#char-to-benchmark').click( function(){
    $.ajaxSettings.async = false;

    let quantificationType = ["qfactor_estimation"];
    $.getJSON( '/benchmark/benchmark_getMeasurement', 
    { measurementType: char_TASK, quantificationType: JSON.stringify(quantificationType) }, 
        function () {
    }); 

    window.open("/benchmark");
    $.ajaxSettings.async = true;
    return false;
    }
);
 
