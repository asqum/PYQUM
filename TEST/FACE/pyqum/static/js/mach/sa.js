//when page is loading:
$(document).ready(function(){
    $('div.sacontent').hide();
    $('div.sacontent.settings').show();
});

//Select model to proceed:
$(function () {
    $('button.sa.saname').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.saname = $(this).attr('id');
        window.satype = saname.split('-')[0];
        console.log(saname)
        // Indicate current instrument we are operating on:
        $("i.sa.fa-check").remove();
        $(this).prepend("<i class='sa fa fa-check' style='font-size:15px;color:green;'></i> ");
        $('select.sa.scale[name="sparam"]').val(""); //reset s-parameter
        // connecting to each models:
        $.getJSON('/mach/sa/connect', {
            saname: saname
        }, function (data) {
            console.log(data.message);
            console.log(data.status);
            $('div.sa#sa-current-user').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.sa."+saname+".fa-refresh" ).remove(); //clear previous icon
            if (data.status=='connected'){
                $('button.sa.saname#'+saname).removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.sacontent').hide();
                $('div.sacontent.settings').show();
                $.getJSON('/mach/sa/get', {
                    saname: saname, satype: satype,
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.sa.settings').addClass('getvalue');
                    // output freq range:
                    var freqrange = data.message['start-frequency'].split(' ')[0] + " to " + data.message['stop-frequency'].split(' ')[0] + " * "
                                        + data.message['step-points'];
                    $('input.sa.scale.settings[name="freqrange"]').val(freqrange);
                    $('input.sa.unit.settings[name="freqrange"]').val(data.message['start-frequency'].split(' ')[1]);
                    // output power (w/ unit), IF-bandwidth (w/ unit) & S-Parameter:
                    $('input.sa.scale.settings[name="powa"]').val(data.message['power'].split(" ")[0]);
                    $('input.sa.unit.settings[name="powa"]').val(data.message['power'].split(' ')[1]);
                    $('input.sa.scale.settings[name="ifb"]').val(data.message['ifb'].split(" ")[0]);
                    $('input.sa.unit.settings[name="ifb"]').val(data.message['ifb'].split(' ')[1]);
                    $('input.sa.sparam[name="S21"]').prop( "checked", Boolean(data.message['s21']) );
                    $('input.sa.sparam[name="S12"]').prop( "checked", Boolean(data.message['s12']) );
                    $('input.sa.sparam[name="S11"]').prop( "checked", Boolean(data.message['s11']) );
                    $('input.sa.sparam[name="S22"]').prop( "checked", Boolean(data.message['s22']) );
                    $('input.sa.sparam[name="S43"]').prop( "checked", Boolean(data.message['s43']) );
                    $('input.sa.sparam[name="S34"]').prop( "checked", Boolean(data.message['s34']) );
                    $('input.sa.sparam[name="S33"]').prop( "checked", Boolean(data.message['s33']) );
                    $('input.sa.sparam[name="S44"]').prop( "checked", Boolean(data.message['s44']) );
                });
            } else if (data.status=='waiting') {
                $('button.sa.saname#'+saname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.sa.saname#'+saname).removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            } else if (data.status=='forbidden') {
                $('button.sa.saname#'+saname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            };
        })
        .done(function(data) {
            $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + saname));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Set each value on change:
// RF Power
$('input.sa[name="powa"]').change( function () { // the enter key code
    $.getJSON('/mach/sa/set/powa', {
        saname: saname, satype: satype,
        powa: $('input.sa.scale[name="powa"]').val()
    }, function (data) {
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.sa.settings[name="powa"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("SETTING " + saname + "'s POWER SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.sa.closet').bind('click', function () {
    $.getJSON('/mach/sa/closet', {
        saname: saname, satype: satype,
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.sa[name="saname"]').find('option[value='+saname+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.sa."+saname+".fa-wifi" ).remove();
            $('button.sa.saname#'+saname).removeClass('wait').removeClass('error').removeClass('connect').addClass('close')
                .prepend("<i class='sa "+saname+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.sa').addClass('error');}         
    })
    .done(function(data) {
        $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSING " + saname + " SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.sa#sa-status-announcement').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});





//show log's page
$('button.sa#log').bind('click', function () { // id become #
    $.getJSON('/mach/sa/log', {
        saname: saname, satype: satype,
    }, function (data) {
        $('div.sacontent').hide();
        $('div.sacontent#log').empty();
        console.log('Based on INSTRLOG, Freq: ' + data.log['frequency']);
        $.each(data.log, function(key, value) {
            $('div.sacontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.sacontent#log').show();
        $('button.sa').removeClass('selected');
        $('button.sa#log').addClass('selected');
    });
    return false;
});

//setting on key-press
// $(function () {
//     $('input.sa.settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.sa.settings').trigger('click'); } }); }); // the enter key code //trigger next click below?
