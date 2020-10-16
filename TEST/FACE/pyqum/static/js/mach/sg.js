//when page is loading:
$(document).ready(function(){
    $('div.sgcontent').hide();
    $('div.sgcontent#settings').show();
});

//declare global variables:
// var sgname;

//Select model to proceed:
$(function () {
    $('button.sg#sgname').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.sgname = $(this).attr('name');
        window.sgtype = sgname.split('-')[0];
        console.log(sgname)
        $("i.sg.fa-check").remove();
        $(this).prepend("<i class='sg fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/sg/connect', {
            sgname: sgname
        }, function (data) {
            console.log(data.message);
            $('div.sg#sg-current-user').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            /* Transform the array into a dict */
            var sgdict = {};
            $.each(data.linkedsg, function(key, values) { sgdict[values] = key; });
            if (sgname in sgdict){
                // $('select.sg[name="sgname"]').find('option[value='+sgname+']').removeClass('close').addClass('connect');
                $( "i.sg."+sgname+".fa-refresh" ).remove(); //clear previous icon
                $('button.sg#sgname[name='+sgname+']').removeClass('error').removeClass('close').addClass('connect')
                // Get ALL value:
                $('div.sgcontent').hide();
                $('div.sgcontent#settings').show();
                $.getJSON('/mach/sg/get', {
                    sgname: sgname, sgtype: sgtype
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.sg#settings').addClass('getvalue');
                    $('input.sg.scale#settings[name="freq"]').val(data.message['frequency'].split(' ')[0]);
                    $('input.sg.unit#settings[name="freq"]').val(data.message['frequency'].split(' ')[1]);
                    $('input.sg.scale#settings[name="powa"]').val(data.message['power'].split(" ")[0]);
                    $('input.sg.unit#settings[name="powa"]').val(data.message['power'].split(' ')[1]);
                    $('input.sg[name="oupt"]').prop( "checked", Boolean(data.message['rfoutput']) );
                });
            } else {$('button.sg#sgname[name='+sgname+']').addClass('error');}
        })
        .done(function(data) {
            $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + sgname));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Set each value on change:
// RF Output
$('input.sg[name="oupt"]').change( function () { // the enter key code
    var oupt = $('input.sg[name="oupt"]').is(':checked')?1:0;
    $.getJSON('/mach/sg/set/oupt', {
        sgname: sgname, sgtype: sgtype, oupt: oupt
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message); 
        if (oupt==1) {
            $('button.sg#sgname[name='+sgname+']').append(" <i class='sg "+sgname+" fa fa-wifi' style='font-size:15px;color:green;'></i>");
        } else {
            $( "i.sg."+sgname+".fa-wifi" ).remove();
        };
    })
    .done(function(data) {
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("RF-PORT TOGGLED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// RF Frequency
$('input.sg[name="freq"]').change( function () { // the enter key code
    $.getJSON('/mach/sg/set/freq', {
        sgname: sgname, sgtype: sgtype,
        freq: $('input.sg.scale[name="freq"]').val(), frequnit: $('input.sg.unit[name="freq"]').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.sg#settings[name="freq"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("FREQUENCY ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// RF Power
$('input.sg[name="powa"]').change( function () { // the enter key code
    $.getJSON('/mach/sg/set/powa', {
        sgname: sgname, sgtype: sgtype,
        powa: $('input.sg.scale[name="powa"]').val(), powaunit: $('input.sg.unit[name="powa"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.sg#settings[name="powa"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("POWER ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

//show log's page
$('button.sg#log').bind('click', function () { // id become #
    $.getJSON('/mach/sg/log', {
        sgname: sgname, sgname: sgname
    }, function (data) {
        $('div.sgcontent').hide();
        $('div.sgcontent#log').empty();
        console.log('Based on INSTRLOG, Freq: ' + data.log['frequency']);
        $.each(data.log, function(key, value) {
            $('div.sgcontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.sgcontent#log').show();
        $('button.sg').removeClass('selected');
        $('button.sg#log').addClass('selected');
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.sg#closet').bind('click', function () {
    $.getJSON('/mach/sg/closet', {
        sgname: sgname, sgtype: sgtype
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.sg[name="sgname"]').find('option[value='+sgname+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.sg."+sgname+".fa-wifi" ).remove();
            $('button.sg#sgname[name='+sgname+']').removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='sg "+sgname+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.sg').addClass('error');}         
    })
    .done(function(data) {
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sg#sg-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});


//setting on key-press
// $(function () {
//     $('input.sg#settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.sg#settings').trigger('click'); } }); }); // the enter key code //trigger next click below?