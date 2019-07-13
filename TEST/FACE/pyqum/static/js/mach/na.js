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
                    // $('input.na.scale#settings[name="freqrange"]').val(data.message['frequency'].split(' ')[0]);
                    // $('input.na.unit#settings[name="freqrange"]').val(data.message['frequency'].split(' ')[1]);
                    $('input.na.scale#settings[name="powa"]').val(data.message['power'].split(" ")[0]);
                    $('input.na.unit#settings[name="powa"]').val(data.message['power'].split(' ')[1]);
                    $('input.na.scale#settings[name="ifb"]').val(data.message['ifb'].split(" ")[0]);
                    $('input.na.unit#settings[name="ifb"]').val(data.message['ifb'].split(' ')[1]);
                    $('input.na.scale#settings[name="ave"]').val(data.message['ave']);
                    $('input.na[name="oupt"]').prop( "checked", Boolean(data.message['rfports']) );
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
        $('input.na#settings[name="freq"]').removeClass('getvalue').addClass('setvalue');
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
// AVERAGE
$('input.na[name="ave"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/ave', {
        natype: natype,
        ave: $('input.na.scale[name="ave"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na#settings[name="ave"]').removeClass('getvalue').addClass('setvalue');
    });
    return false;
});
// S-Parameter
$('select.na[name="sparam"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/sparam', {
        natype: natype,
        sparam: $('select.na.scale[name="sparam"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na#settings[name="sparam"]').removeClass('getvalue').addClass('setvalue');
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

// Preset
$('button.na#preset').bind('click', function () {
    $.getJSON('/mach/na/preset', {
        natype: natype
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $( "i.na."+natype+".fa-wifi" ).remove();
            $('button.na#natype[name='+natype+']').removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='na "+natype+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.na').addClass('error');}         
    });
    return false;
});

// RF SWEEP (CONT)
// $(function () {
//     $('input.na#settings[name="sweep"]').click( function () { // the enter key code
//         var swpstat = $('input.na#settings[name="sweep"]').is(':checked');
//         if (swpstat == true) {
//             var sweeploop = setInterval( function() {
//                 // $.getJSON('/mach/na/set/sweep', {
//                 //     natype: natype
//                 // }, function (data) {    
//                 // });
//                 console.log("sweep");
//             }, 1000);
//             $('input.na#settings[name="sweep"]').click( function () {
//                 clearInterval(sweeploop);
//             });
//         };
//     });
// });
$(function(){
    $('input.na#settings[name="sweep"]').click( function () { // the enter key code
    var swpstat = $('input.na#settings[name="sweep"]').is(':checked');
    do {
        // $.getJSON('/mach/na/set/sweep', {
        //     natype: natype
        // }, function (data) {    
        // });
        console.log("sweep");
    } while (swpstat == true);
    });
});



//setting on key-press
// $(function () {
//     $('input.na#settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.na#settings').trigger('click'); } }); }); // the enter key code //trigger next click below?