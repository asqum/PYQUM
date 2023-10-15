$(document).ready(function(){
    // $('div.qcirccontent').show();
    
});

// click to RUN:
$('input.guid#guid-qcirc-qasm-run').on('touchend click', function(event) {
    eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
    console.log("running quantum circuit")
    var qasm_script = JSON.stringify($('textarea.guid#guid-qcirc-qasm-script').val());
    
    // START RUNNING
    $.getJSON(mssnencrpytonian() + '/mssn/oqc/receive', {
        composer: 0, 
        backend: $('select.guid#guid-qcirc-backend').val(),
        shots: $('input.guid#guid-qcirc-shots').val(),
        qasm: qasm_script,
    }, function (data) {   
        console.log(JSON.stringify(data.circuit_map));    
        // $('h4#guid-qcirc-map').text(data.circuit_map);
        $('h4#guid-qcirc-result').text(data.message + ": " + JSON.stringify(data.result));
    });

    return false;
});


