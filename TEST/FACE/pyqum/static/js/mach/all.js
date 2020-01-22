//when page is loading:
$(document).ready(function(){
    // $('div.all.good').hide()
    setInterval(digitalclock, 1000);
    function digitalclock(){
        $('div.all.clock').empty();
        $('div.all.clock').append($('<h4 style="background-color: yellow;"></h4>').text(Date($.now())));
        $.getJSON('/mach/all/status', { }, function(data) {
            
            if (data.status.PSGV == 'disconnected') {
                $('input.all.mach#psgv-status').prop( "checked", Boolean(1) );
            } else if (data.status.PSGV == 'connected') {
                $('input.all.mach#psgv-status').prop( "checked", Boolean(0) );
            };

            if (data.status.AWG == 'closed') {
                $('input.all.mach#awg-status').prop( "checked", Boolean(1) );
            } else if (data.status.AWG == 'initialized') {
                $('input.all.mach#awg-status').prop( "checked", Boolean(0) );
            };

        });
            
    }
});


$('input[type="checkbox"]').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
});


