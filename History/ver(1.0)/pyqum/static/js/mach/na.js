//when page is loading:
$(document).ready(function(){
    $('div.nacontent').hide();
    $('div.nacontent#settings').show();
});

//declare global variables:
// var natype;

//Select model to proceed:
$(function () {
    $('button.na#natype').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.natype = $(this).attr('name');
        console.log(natype)
        $("i.na.fa-check").remove();
        $(this).prepend("<i class='na fa fa-check' style='font-size:15px;color:green;'></i> ");
        $('select.na.scale[name="sparam"]').val(""); //reset s-parameter
        // connecting to each models:
        $.getJSON('/mach/na/connect', {
            natype: natype
        }, function (data) {
            console.log(data.message);
            /* Transform the array into a dict */
            var nadict = {};
            $.each(data.linkedna, function(key, values) { nadict[values] = key; });
            if (natype in nadict){
                // $('select.na[name="natype"]').find('option[value='+natype+']').removeClass('close').addClass('connect');
                $( "i.na."+natype+".fa-refresh" ).remove(); //clear previous icon
                $('button.na#natype[name='+natype+']').removeClass('error').removeClass('close').addClass('connect')
                // Get ALL value:
                $('div.nacontent').hide();
                $('div.nacontent#settings').show();
                $.getJSON('/mach/na/get', {
                    natype: natype
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.na#settings').addClass('getvalue');
                    // output freq range:
                    var freqrange = data.message['start-frequency'].split(' ')[0] + " to " + data.message['stop-frequency'].split(' ')[0] + " * "
                                        + data.message['step-points'];
                    $('input.na.scale#settings[name="freqrange"]').val(freqrange);
                    $('input.na.unit#settings[name="freqrange"]').val(data.message['start-frequency'].split(' ')[1]);
                    // output power (w/ unit), IF-bandwidth (w/ unit) & S-Parameter:
                    $('input.na.scale#settings[name="powa"]').val(data.message['power'].split(" ")[0]);
                    $('input.na.unit#settings[name="powa"]').val(data.message['power'].split(' ')[1]);
                    $('input.na.scale#settings[name="ifb"]').val(data.message['ifb'].split(" ")[0]);
                    $('input.na.unit#settings[name="ifb"]').val(data.message['ifb'].split(' ')[1]);
                    $('input.na.sparam[name="S21"]').prop( "checked", Boolean(data.message['s21']) );
                });
            } else {$('button.na#natype[name='+natype+']').addClass('error');}
        });
        return false;
    });
}); 
 
// Set each value on change:
// RF Frequency Range
$('input.na[name="freqrange"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/freqrange', {
        natype: natype,
        freqrange: $('input.na.scale[name="freqrange"]').val(), frequnit: $('input.na.unit[name="freqrange"]').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na#settings[name="freqrange"]').removeClass('getvalue').addClass('setvalue');
    });
    return false;
});
// RF Power
$('input.na[name="powa"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/powa', {
        natype: natype,
        powa: $('input.na.scale[name="powa"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na#settings[name="powa"]').removeClass('getvalue').addClass('setvalue');
    });
    return false;
});
// IFB
$('input.na[name="ifb"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/ifb', {
        natype: natype,
        ifb: $('input.na.scale[name="ifb"]').val(),
        ifbunit: $('input.na.unit[name="ifb"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na#settings[name="ifb"]').removeClass('getvalue').addClass('setvalue');
    });
    return false;
});
// Scanning
$('input.na[name="scanning"]').change( function () { // the enter key code
    var scan = $('input.na[name="scanning"]').is(':checked')?1:0;
    $.getJSON('/mach/na/set/scanning', {
        natype: natype, scan: scan
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message); 
        if (scan==1) {
            $('button.na#natype[name='+natype+']').append(" <i class='na "+natype+" fa fa-wifi' style='font-size:15px;color:green;'></i>");
        } else {
            $( "i.na."+natype+".fa-wifi" ).remove();
        };
    });
    return false;
});


//show log's page
$('button.na#log').bind('click', function () { // id become #
    $.getJSON('/mach/na/log', {
        natype: natype
    }, function (data) {
        $('div.nacontent').hide();
        $('div.nacontent#log').empty();
        console.log('Based on INSTRLOG, Freq: ' + data.log['frequency']);
        $.each(data.log, function(key, value) {
            $('div.nacontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.nacontent#log').show();
        $('button.na').removeClass('selected');
        $('button.na#log').addClass('selected');
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.na#closet').bind('click', function () {
    $.getJSON('/mach/na/closet', {
        natype: natype
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.na[name="natype"]').find('option[value='+natype+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.na."+natype+".fa-wifi" ).remove();
            $('button.na#natype[name='+natype+']').removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='na "+natype+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.na').addClass('error');}         
    });
    return false;
});

// SWEEP
$(function(){
    $('button.na#sweep').click( function () { // the enter key code
        $( "i.na" ).remove(); //clear previous
        $("button.na[name="+natype+"]").prepend("<i class='na fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var s21 = $('input.na.sparam#settings[name="S21"]').is(':checked')?1:0;
        var s11 = $('input.na.sparam#settings[name="S11"]').is(':checked')?1:0;
        var s12 = $('input.na.sparam#settings[name="S12"]').is(':checked')?1:0;
        var s22 = $('input.na.sparam#settings[name="S22"]').is(':checked')?1:0;
            
        $.getJSON('/mach/na/set/sweep', {
            natype: natype, s21: s21, s11: s11, s12: s12, s22: s22
        }, function (data) {  
            console.log("sweep complete: " + data.sweep_complete);  
            console.log("ETA in " + data.swptime + 's');
            $( "i.na" ).remove(); //clear processing animation
        });
            
        return false;
    });
});

// AUTOSCALE
$(function(){
    $('button.na#autoscale').click( function () { // the enter key code
        $.getJSON('/mach/na/set/autoscale', {
            natype: natype
        }, function (data) {  
            console.log("status: " + data.message);  
        });  
        return false;
    });
});


//setting on key-press
// $(function () {
//     $('input.na#settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.na#settings').trigger('click'); } }); }); // the enter key code //trigger next click below?