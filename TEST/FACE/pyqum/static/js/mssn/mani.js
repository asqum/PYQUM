//when page is loading:
$(document).ready(function(){
    $('div.manicontent').hide();
    window.mani_TASK = "";
    return false;
});

// RETURN to Sample selection page:
$('input.mani.loaded#sample-name').on('click', function() {
    window.location.href='/auth/user';
    return false;
});

$('button.mani.access.singleqb').on('click', function() { mani_TASK = 'singleqb' });
$('button.mani.access.qubits').on('click', function() { mani_TASK = 'qubits' });

// Event: Benchmark on click (Jacky)
$('#mani-to-benchmark').click( function(){
    
    $.ajaxSettings.async = false;

    // listimes_singleqb();
    // accessdata_singleqb();
    // $.getJSON(mssnencrpytonian() + '/mssn/singleqb/access', 
    //     { wmoment: wmoment },
    //     //input/select value here:  
    //     function (data) {
    //         //console.log("JOBID: " + JSON.stringify(data.JOBID) );
    //         console.log( data );  
                    
    // });
    let quantificationType = ["qfactor_estimation"];
    $.getJSON( '/benchmark/benchmark_getMeasurement', 
    { measurementType: mani_TASK, quantificationType: JSON.stringify(quantificationType) }, 
        function ( ) {
    }); 

    setTimeout(() => { $('div.navbar button.benchmark').trigger('click'); }, 101);
    $.ajaxSettings.async = true;

    return false;
    }
);
 
