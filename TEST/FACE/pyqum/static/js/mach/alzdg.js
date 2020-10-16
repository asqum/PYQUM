//when page is loading:
$(document).ready(function(){
    $('div.alzdgcontent').hide();
    $('div.alzdgcontent#settings').show();
});

//declare global variables:
// var alzdglabel;

//Select model to connect and proceed:
$(function () {
    $('button.alzdg.label').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.alzdglabel = $(this).attr('id');
        console.log(alzdglabel)
        $("i.alzdg.fa-check").remove();
        $(this).prepend("<i class='alzdg fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/alzdg/connect', {
            alzdglabel: alzdglabel
        }, function (data) {
            console.log(data.message);
            /* Transform the array into a dict */
            var alzdgdict = {};
            $.each(data.linkedalzdg, function(key, values) { alzdgdict[values] = key; });
            if (alzdglabel in alzdgdict){
                // $('select.alzdg[name="alzdglabel"]').find('option[value='+alzdglabel+']').removeClass('close').addClass('connect');
                $( "i.alzdg."+alzdglabel+".fa-refresh" ).remove(); //clear previous icon
                $('button.alzdg.label#'+alzdglabel).removeClass('error').removeClass('close').addClass('connect')
                // Get ALL value:
                $('div.alzdgcontent').hide();
                $('div.alzdgcontent#settings').show();
                $.getJSON('/mach/alzdg/get', {
                    alzdglabel: alzdglabel
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.alzdg#settings').addClass('getvalue');
                    // $('input.alzdg.scale.settings#clockfreq').val(data.message['clockfreq'].split(' ')[0]);
                    // $('input.alzdg.unit.settings#clockfreq').val(data.message['clockfreq'].split(' ')[1]);
                    // $('input.alzdg[name="oupt"]').prop( "checked", Boolean(data.message['rfoutput']) );

                    // Query only output:
                    $('div.alzdg#alzdg-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model']));
                });
            } else {$('button.alzdg.label#'+alzdglabel).addClass('error');}
        })
        .done(function(data) {
            $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + alzdglabel));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Setting Waveform Output


//show log's page
$('button.alzdg#log').bind('click', function () { // id become #
    $.getJSON('/mach/alzdg/log', {
        alzdglabel: alzdglabel
    }, function (data) {
        $('div.alzdgcontent').hide();
        $('div.alzdgcontent#log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.alzdgcontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.alzdgcontent#log').show();
        $('button.alzdg').removeClass('selected');
        $('button.alzdg#log').addClass('selected');
    });
    return false;
});

// Test the flow / script for use in measurement
$('button.alzdg#testing').bind('click', function () {
    $( "i.alzdg.fa-cog" ).remove(); //clear previous
    $('button.alzdg.label#' + alzdglabel).prepend("<i class='alzdg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/alzdg/testing', {
        alzdglabel: alzdglabel
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $( "i.alzdg.fa-cog" ).remove();
            
        } else {$('button.alzdg').addClass('error');}         
    })
    .done(function(data) {
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: blue;"></h4>').text("TEST-FLOW SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
