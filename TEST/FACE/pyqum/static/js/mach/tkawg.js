//when page is loading:
$(document).ready(function(){
    $('div.tkawgcontent').hide();
    $('div.tkawgcontent#settings').show();
});

//declare global variables:
// var tkawglabel;

//Select model to proceed:
$(function () {
    $('button.tkawg.label').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.tkawglabel = $(this).attr('id');
        console.log(tkawglabel)
        $("i.tkawg.fa-check").remove();
        $(this).prepend("<i class='tkawg fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/tkawg/connect', {
            tkawglabel: tkawglabel
        }, function (data) {
            console.log(data.message);
            /* Transform the array into a dict */
            var tkawgdict = {};
            $.each(data.linkedtkawg, function(key, values) { tkawgdict[values] = key; });
            if (tkawglabel in tkawgdict){
                // $('select.tkawg[name="tkawglabel"]').find('option[value='+tkawglabel+']').removeClass('close').addClass('connect');
                $( "i.tkawg."+tkawglabel+".fa-refresh" ).remove(); //clear previous icon
                $('button.tkawg.label#'+tkawglabel).removeClass('error').removeClass('close').addClass('connect')
                // Get ALL value:
                $('div.tkawgcontent').hide();
                $('div.tkawgcontent#settings').show();
                $.getJSON('/mach/tkawg/get', {
                    tkawglabel: tkawglabel
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.tkawg#settings').addClass('getvalue');
                    $('input.tkawg.scale.settings#clockfreq').val(data.message['clockfreq'].split(' ')[0]);
                    $('input.tkawg.unit.settings#clockfreq').val(data.message['clockfreq'].split(' ')[1]);
                    // $('input.tkawg[name="oupt"]').prop( "checked", Boolean(data.message['rfoutput']) );

                    // Query only output:
                    $('div.tkawg#tkawg-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model']));
                });
            } else {$('button.tkawg.label#'+tkawglabel).addClass('error');}
        })
        .done(function(data) {
            $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + tkawglabel));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Setting Waveform Output
// $('input.tkawg[name="oupt"]').change( function () { // the enter key code
//     var oupt = $('input.tkawg[name="oupt"]').is(':checked')?1:0;
//     $.getJSON('/mach/tkawg/set/oupt', {
//         tkawglabel: tkawglabel, oupt: oupt
//     }, function (data) { 
//         console.log(Date($.now()) + ':\nSetting ' + data.message); 
//         if (oupt==1) {
//             $('button.tkawg.label#'+tkawglabel).append(" <i class='tkawg "+tkawglabel+" fa fa-wifi' style='font-size:15px;color:green;'></i>");
//         } else {
//             $( "i.tkawg."+tkawglabel+".fa-wifi" ).remove();
//         };
//     })
//     .done(function(data) {
//         $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("RF-PORT TOGGLED SUCCESSFULLY"));
//     })
//     .fail(function(jqxhr, textStatus, error){
//         $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
//     });
//     return false;
// });

// Setting Clock Frequency
$('input.tkawg#clockfreq').change( function () { // the enter key code
    $.getJSON('/mach/tkawg/set/clockfreq', {
        tkawglabel: tkawglabel,
        clockfreq: $('input.tkawg.scale#clockfreq').val(), clockfrequnit: $('input.tkawg.unit#clockfreq').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.tkawg#settings[name="freq"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("FREQUENCY ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

//show log's page
$('button.tkawg#log').bind('click', function () { // id become #
    $.getJSON('/mach/tkawg/log', {
        tkawglabel: tkawglabel
    }, function (data) {
        $('div.tkawgcontent').hide();
        $('div.tkawgcontent#log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.tkawgcontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.tkawgcontent#log').show();
        $('button.tkawg').removeClass('selected');
        $('button.tkawg#log').addClass('selected');
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.tkawg#closet').bind('click', function () {
    $.getJSON('/mach/tkawg/closet', {
        tkawglabel: tkawglabel
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.tkawg[name="tkawglabel"]').find('option[value='+tkawglabel+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.tkawg."+tkawglabel+".fa-wifi" ).remove();
            $('button.tkawg.label#'+tkawglabel).removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='tkawg "+tkawglabel+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.tkawg').addClass('error');}         
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// Test the flow / script for use in measurement
$('button.tkawg#testing').bind('click', function () {
    $( "i.tkawg.fa-cog" ).remove(); //clear previous
    $('button.tkawg.label#' + tkawglabel).prepend("<i class='tkawg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/tkawg/testing', {
        tkawglabel: tkawglabel
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $( "i.tkawg.fa-cog" ).remove();
            
        } else {$('button.tkawg').addClass('error');}         
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("TEST-FLOW SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
