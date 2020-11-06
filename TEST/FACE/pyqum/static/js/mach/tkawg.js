//when page is loading:
$(document).ready(function(){
    $('div.tkawgcontent').hide();
    $('div.tkawgcontent.settings').show();
});

//Select model to proceed:
$(function () {
    $('button.tkawg.label').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.tkawglabel = $(this).attr('id');
        console.log(tkawglabel)
        // Indicate current instrument we are operating on:
        $("i.tkawg.fa-check").remove();
        $(this).prepend("<i class='tkawg fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/tkawg/connect', {
            tkawglabel: tkawglabel
        }, function (data) {
            console.log(data.message);
            $('div.tkawg#tkawg-activity').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.tkawg."+tkawglabel+".fa-refresh" ).remove(); //clear previous icon
            // check status
            if (data.status=='connected'){
                $('button.tkawg.label#'+tkawglabel).removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.tkawgcontent').hide();
                $('div.tkawgcontent.settings').show();
                $.getJSON('/mach/tkawg/get', {
                    tkawglabel: tkawglabel
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.tkawg.settings').addClass('getvalue');
                    $('input.tkawg.scale.settings.clockfreq').val(data.message['clockfreq'].split(' ')[0]);
                    $('input.tkawg.unit.settings.clockfreq').val(data.message['clockfreq'].split(' ')[1]);
                    // $('input.tkawg[name="oupt"]').prop( "checked", Boolean(data.message['rfoutput']) );

                    // Query only output:
                    $('div.tkawg#tkawg-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model']));
                });
            } else if (data.status=='waiting') {
                $('button.tkawg.label#'+tkawglabel).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.tkawg.label#'+tkawglabel).removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            };
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
$('input.tkawg.clockfreq').change( function () { // the enter key code
    $.getJSON('/mach/tkawg/set/clockfreq', {
        tkawglabel: tkawglabel,
        clockfreq: $('input.tkawg.scale.clockfreq').val(), clockfrequnit: $('input.tkawg.unit.clockfreq').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.tkawg.settings.clockfreq').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOCK-FREQUENCY ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.tkawg.closet').bind('click', function () {
    $.getJSON('/mach/tkawg/closet', {
        tkawglabel: tkawglabel
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.tkawg[name="tkawglabel"]').find('option[value='+tkawglabel+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.tkawg."+tkawglabel+".fa-wifi" ).remove();
            $('button.tkawg.label#'+tkawglabel).removeClass('error').removeClass('wait').removeClass('connect').addClass('close')
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

// All Off
$('button.tkawg#tkawg-alloff').bind('click', function () {
    $( "i.tkawg.fa-cog" ).remove(); //clear previous
    $('button.tkawg.label#' + tkawglabel).prepend("<i class='tkawg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/tkawg/alloff', {
        tkawglabel: tkawglabel
    }, function (data) {
        console.log("All-Off: " + data.message);
        if (data.message[0] == "success"){
            $( "i.tkawg.fa-cog" ).remove();
        } else {$('button.tkawg').addClass('error');}         
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("ALL-OFF SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// Clear ALL (Waveform)
$('button.tkawg#tkawg-clearall').bind('click', function () {
    $( "i.tkawg.fa-cog" ).remove(); //clear previous
    $('button.tkawg.label#' + tkawglabel).prepend("<i class='tkawg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/tkawg/clearall', {
        tkawglabel: tkawglabel
    }, function (data) {
        console.log("Clear-All: " + data.message);
        $( "i.tkawg.fa-cog" ).remove();         
    })
    .done(function(data) {
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLEAR ALL WAVEFORM SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// Test the flow / script for use in measurement
$('button.tkawg#tkawg-testing').bind('click', function () {
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

//show log's page
$('button.tkawg.log').bind('click', function () {
    // Indicate current spec we are inspecting on current instrument:
    $("i.tkawg.fa-angle-double-right").remove();
    $(this).prepend("<i class='tkawg fas fa-angle-double-right' style='font-size:15px;color:black;'></i> ");
    $.getJSON('/mach/tkawg/log', {
        tkawglabel: tkawglabel
    }, function (data) {
        $('div.tkawgcontent').hide();
        $('div.tkawgcontent.log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.tkawgcontent.log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.tkawgcontent.log').show();
        $('button.tkawg').removeClass('selected');
        $('button.tkawg.log').addClass('selected');
    });
    return false;
});

// Getting & Setting Channel:
$('button.tkawg.channels').bind('click', function () {
    // Which Channel:
    window.Channel = $(this).attr('name').split('-')[1];
    console.log("Setting Channel-" + Channel);
    // Indicate current spec we are inspecting on current instrument:
    $("i.tkawg.fa-angle-double-right").remove();
    $(this).prepend("<i class='tkawg fas fa-angle-double-right' style='font-size:15px;color:black;'></i> ");
    $.getJSON('/mach/tkawg/get/channels', {
        tkawglabel: tkawglabel, Channel: Channel
    }, function (data) {
        $('div.tkawgcontent').hide();
        $('div.tkawgcontent.setchannels').show();
        console.log(data.message);
        $('input.tkawg.scale.source-amplitude').val(data.message['source-amplitude'].split(' ')[0]);
        $('input.tkawg.unit.source-amplitude').val(data.message['source-amplitude'].split(' ')[1]);
        $('input.tkawg.scale.source-offset').val(data.message['source-offset'].split(' ')[0]);
        $('input.tkawg.unit.source-offset').val(data.message['source-offset'].split(' ')[1]);
        $('button.tkawg').removeClass('selected');
        $('button.tkawg.channels[name="channel-' + Channel + '"]').addClass('selected');
    });
    return false;
});
$('input.tkawg.setchannels').change( function () { // the enter key code
    $.getJSON('/mach/tkawg/set/channels', {
        sgname: sgname, sgtype: sgtype,
        powa: $('input.sg.scale[name="powa"]').val(), powaunit: $('input.sg.unit[name="powa"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.sg.settings[name="powa"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text(sgname + "'s POWER ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});