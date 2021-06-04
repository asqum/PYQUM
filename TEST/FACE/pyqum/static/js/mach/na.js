//when page is loading:
$(document).ready(function(){
    $('div.nacontent').hide();
    $('div.nacontent.settings').show();
});

//Select model to proceed:
$(function () {
    $('button.na.naname').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.naname = $(this).attr('id');
        window.natype = naname.split('-')[0];
        console.log(naname)
        // Indicate current instrument we are operating on:
        $("i.na.fa-check").remove();
        $(this).prepend("<i class='na fa fa-check' style='font-size:15px;color:green;'></i> ");
        $('select.na.scale[name="sparam"]').val(""); //reset s-parameter
        // connecting to each models:
        $.getJSON('/mach/na/connect', {
            naname: naname
        }, function (data) {
            console.log(data.message);
            $('div.na#na-current-user').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.na."+naname+".fa-refresh" ).remove(); //clear previous icon
            if (data.status=='connected'){
                $('button.na.naname#'+naname).removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.nacontent').hide();
                $('div.nacontent.settings').show();
                $.getJSON('/mach/na/get', {
                    naname: naname, natype: natype,
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.na.settings').addClass('getvalue');
                    // output freq range:
                    var freqrange = data.message['start-frequency'].split(' ')[0] + " to " + data.message['stop-frequency'].split(' ')[0] + " * "
                                        + data.message['step-points'];
                    $('input.na.scale.settings[name="freqrange"]').val(freqrange);
                    $('input.na.unit.settings[name="freqrange"]').val(data.message['start-frequency'].split(' ')[1]);
                    // output power (w/ unit), IF-bandwidth (w/ unit) & S-Parameter:
                    $('input.na.scale.settings[name="powa"]').val(data.message['power'].split(" ")[0]);
                    $('input.na.unit.settings[name="powa"]').val(data.message['power'].split(' ')[1]);
                    $('input.na.scale.settings[name="ifb"]').val(data.message['ifb'].split(" ")[0]);
                    $('input.na.unit.settings[name="ifb"]').val(data.message['ifb'].split(' ')[1]);
                    $('input.na.sparam[name="S21"]').prop( "checked", Boolean(data.message['s21']) );
                    $('input.na.sparam[name="S12"]').prop( "checked", Boolean(data.message['s12']) );
                    $('input.na.sparam[name="S11"]').prop( "checked", Boolean(data.message['s11']) );
                    $('input.na.sparam[name="S22"]').prop( "checked", Boolean(data.message['s22']) );
                    $('input.na.sparam[name="S43"]').prop( "checked", Boolean(data.message['s43']) );
                    $('input.na.sparam[name="S34"]').prop( "checked", Boolean(data.message['s34']) );
                    $('input.na.sparam[name="S33"]').prop( "checked", Boolean(data.message['s33']) );
                    $('input.na.sparam[name="S44"]').prop( "checked", Boolean(data.message['s44']) );
                });
            } else if (data.status=='waiting') {
                $('button.na.naname#'+naname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.na.naname#'+naname).removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            } else if (data.status=='forbidden') {
                $('button.na.naname#'+naname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            };
        })
        .done(function(data) {
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + naname));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Set each value on change:
// RF Frequency Range
$('input.na[name="freqrange"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/freqrange', {
        naname: naname, natype: natype,
        freqrange: $('input.na.scale[name="freqrange"]').val(), frequnit: $('input.na.unit[name="freqrange"]').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na.settings[name="freqrange"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("SETTING " + naname + "'s FREQUENCY RANGE SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// RF Power
$('input.na[name="powa"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/powa', {
        naname: naname, natype: natype,
        powa: $('input.na.scale[name="powa"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na.settings[name="powa"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("SETTING " + naname + "'s POWER SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// IFB
$('input.na[name="ifb"]').change( function () { // the enter key code
    $.getJSON('/mach/na/set/ifb', {
        naname: naname, natype: natype,
        ifb: $('input.na.scale[name="ifb"]').val(),
        ifbunit: $('input.na.unit[name="ifb"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.na.settings[name="ifb"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("SETTING " + naname + "'s IF-BANDWIDTH SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// Scanning
$('input.na[name="scanning"]').change( function () { // the enter key code
    var scan = $('input.na[name="scanning"]').is(':checked')?1:0;
    $.getJSON('/mach/na/set/scanning', {
        naname: naname, natype: natype, scan: scan
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message); 
        if (scan==1) {
            $('button.na.naname#'+naname).append(" <i class='na "+naname+" fa fa-wifi' style='font-size:15px;color:green;'></i>");
        } else {
            $( "i.na."+naname+".fa-wifi" ).remove();
        };
    })
    .done(function(data) {
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text(naname + " SCANNING CONTINUOUSLY: " + Boolean(scan)));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.na.closet').bind('click', function () {
    $.getJSON('/mach/na/closet', {
        naname: naname, natype: natype,
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.na[name="naname"]').find('option[value='+naname+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.na."+naname+".fa-wifi" ).remove();
            $('button.na.naname#'+naname).removeClass('wait').removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='na "+naname+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.na').addClass('error');}         
    })
    .done(function(data) {
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSING " + naname + " SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// SWEEP
$(function(){
    $('button.na#sweep').click( function () { // the enter key code
        $( "i.na" ).remove(); //clear previous
        $('button.na.naname#'+naname).prepend("<i class='na fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var s21 = $('input.na.sparam.settings[name="S21"]').is(':checked')?1:0;
        var s11 = $('input.na.sparam.settings[name="S11"]').is(':checked')?1:0;
        var s12 = $('input.na.sparam.settings[name="S12"]').is(':checked')?1:0;
        var s22 = $('input.na.sparam.settings[name="S22"]').is(':checked')?1:0;
        var s43 = $('input.na.sparam.settings[name="S43"]').is(':checked')?1:0;
        var s33 = $('input.na.sparam.settings[name="S33"]').is(':checked')?1:0;
        var s34 = $('input.na.sparam.settings[name="S34"]').is(':checked')?1:0;
        var s44 = $('input.na.sparam.settings[name="S44"]').is(':checked')?1:0;
            
        $.getJSON('/mach/na/set/sweep', {
            naname: naname, natype: natype, s21: s21, s11: s11, s12: s12, s22: s22, s43: s43, s33: s33, s34: s34, s44: s44
        }, function (data) {  
            console.log("sweep complete: " + data.sweep_complete);  
            console.log("ETA in " + data.swptime + 's');
            $( "i.na" ).remove(); //clear processing animation
        })
        .done(function(data) {
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("SWEEPING " + naname + " SUCCESSFULLY"));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });  
        return false;
    });
});

// AUTOSCALE
$(function(){
    $('button.na#autoscale').click( function () { // the enter key code
        $.getJSON('/mach/na/set/autoscale', {
            naname: naname, natype: natype,
        }, function (data) {  
            console.log("status: " + data.message);  
        })
        .done(function(data) {
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text(naname + " SUCCESSFULLY AUTO-SCALED"));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.na#na-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });  
        return false;
    });
});

//show log's page
$('button.na#log').bind('click', function () { // id become #
    $.getJSON('/mach/na/log', {
        naname: naname, natype: natype,
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

//setting on key-press
// $(function () {
//     $('input.na.settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.na.settings').trigger('click'); } }); }); // the enter key code //trigger next click below?
