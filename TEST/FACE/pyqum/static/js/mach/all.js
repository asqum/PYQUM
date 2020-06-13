//when page is loading:
$(document).ready(function(){
    // $('div.all.good').hide()
    // setInterval(digitalclock, 1000);
});

function digitalclock(){
    $('div.all.clock').empty();
    $('div.all.clock').append($('<h4 style="background-color: yellow;"></h4>').text(Date($.now())));   
}

$('button.all.mach#all-status-update').on('click', function() {
    $.getJSON('/mach/all/status', { }, function(data) {
        // Seems like GET REQUEST is a burden for the network!
        console.log("Loading all instruments' status: ");
        $('input.all.mach#psgv-status').val( "PSGV: " + data.status.PSGV );
        $('input.all.mach#awg-status').val( "AWG: " + data.status.AWG );
    }); 
});

