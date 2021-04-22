//when page is loading:
$(document).ready(function(){
    $('div.tkawgcontent').hide();
    $('div.tkawgcontent.settings').show();
    $('textarea.tkawg.score.setchannels').val("ns=8000;\n");
    // Globals:
    window.music =[[]]; 
    window.musicname = [];
    window.musicolor = [];
});

// Functions:
function awgmultiplot(xdata,YDATA,Yname,Ycolor,xtitle,ytitle) {
    // console.log(xtitle);
    
    var Trace = [];
    $.each(YDATA, function(i,ydata) {
        Trace.push({
            x: xdata, y: ydata, mode: 'lines', type: 'scattergl', name: Yname[i],
            line: {color: Ycolor[i], width: 2.5},
        yaxis: 'y' });
    });

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.66,
        width: $(window).width()*0.7,
        xaxis: {
            zeroline: false,
            title: xtitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 3,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        yaxis: {
            zeroline: false,
            title: ytitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        title: 'Digitized IQ Signal',
        annotations: [{
            xref: 'paper',
            yref: 'paper',
            x: 0.03,
            xanchor: 'right',
            y: 1.05,
            yanchor: 'bottom',
            text: '',
            font: {size: 18},
            showarrow: false,
            textangle: 0
          }]
        };

    Plotly.react('tkawg-IQAP-chart', Trace, layout);
};

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

                    // Checking Play/Run State:
                    $('button.tkawg.label#' + tkawglabel + ' i.tkawg.fas.fa-wave-square').remove();
                    if(data.message['runstate']==2) {
                        $('button.tkawg.label#' + tkawglabel).append("<i class='tkawg fas fa-wave-square fa-spin fa-3x fa-fw' style='font-size:15px;color:black;'></i> ");
                    };

                    // Checking Waveform-Data inside AWG:
                    $.each(data.message['wlist'], function(i,val) {
                        console.log(i + ". wave-" + val);
                        $('button.tkawg.channels[name="channel-' + val + '"]' + " i.tkawg.fa-angle-double-left").remove();
                        $('button.tkawg.channels[name="channel-' + val + '"]').append("<i class='tkawg fas fa-angle-double-left' style='font-size:15px;color:black;'></i> ");
                    });

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

// Getting Channel:
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
        $('textarea.tkawg.score.setchannels').val(data.message['score']);
        $('input.tkawg.scale.source-amplitude').val(data.message['source-amplitude'].split(' ')[0]);
        $('input.tkawg.unit.source-amplitude').val(data.message['source-amplitude'].split(' ')[1]);
        $('input.tkawg.scale.source-offset').val(data.message['source-offset'].split(' ')[0]);
        $('input.tkawg.unit.source-offset').val(data.message['source-offset'].split(' ')[1]);
        $('input.tkawg.setchannels.output').prop( "checked", Boolean(data.message['chstate']) );
        $('button.tkawg').removeClass('selected');
        $('button.tkawg.channels[name="channel-' + Channel + '"]').addClass('selected');
    });
    return false;
});

// Initiate Score with Pulse-period:
$("input.tkawg.initscore").bind('click', function () {
    var pperiod = $('input.tkawg.scale.setchannels.pulse-period').val();
    var pperiodunit = $('input.tkawg.unit.setchannels.pulse-period').val();
    $('textarea.tkawg.score.setchannels').val(pperiodunit + "=" + pperiod + ";\n");
    $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SCORE INITIATED WITH LENGTH " + pperiod + pperiodunit));
    return false;
});
// Inserting shapes into score sheet:
$('input.tkawg.shapes.setchannels').bind('click', function () {
    var lascore = $('textarea.tkawg.score.setchannels').val();
    $('textarea.tkawg.score.setchannels').val(lascore + $(this).val() + '/,' + $('input.tkawg.scale.setchannels.pulse-width').val() + ',' 
                                                                        + $('input.tkawg.scale.setchannels.pulse-height').val() + ';\n');
    console.log('adding: ' + $(this).val());
    return false;
});

// Score (Injecting  waveform-data into AWG):
$('button#tkawg-score').click( function () {
    $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text("SETTING CHANNEL " + Channel));
    var ccolor = ['blue','red','cyan','magenta'];
    $.getJSON('/mach/tkawg/set/channels', {
        tkawglabel: tkawglabel, Channel: Channel,
        maxlvl: $('input.tkawg.scale.source-amplitude').val(),
        maxlvlunit: $('input.tkawg.unit.source-amplitude').val(),
        score: $('textarea.tkawg.score.setchannels').val()
    }, function (data) {
        musicname[parseInt(Channel)-1] = "CH-" + Channel;
        musicolor[parseInt(Channel)-1] = ccolor[parseInt(Channel)-1]
        music[parseInt(Channel)-1] = data.music;
        awgmultiplot(data.timeline, music, musicname, musicolor, 'time', 'waveform');
    })
    .done(function(data) {
        $('button.tkawg.channels[name="channel-' + Channel + '"]').trigger('click');
        $('button.tkawg.channels[name="channel-' + Channel + '"]' + " i.tkawg.fa-angle-double-left").remove();
        $('button.tkawg.channels[name="channel-' + Channel + '"]').append("<i class='tkawg fas fa-angle-double-left' style='font-size:15px;color:black;'></i> ");
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SET CHANNEL " + Channel + " SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// Set Channel State:
$('input.tkawg.setchannels.output').change(function () {
    var state = $('input.tkawg.setchannels.output').is(':checked')?1:0;
    $.getJSON('/mach/tkawg/output/channels', {
        tkawglabel: tkawglabel, Channel: Channel, state: state,
    }, function (data) {
        var status = data.status;
    })
    .done(function(data) {
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SET CHANNEL " + Channel + ": " + Boolean(state)));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\n" + status + "\nPlease Refresh!"));
    });
    return false;
});
// PLAY
$('button#tkawg-play').click( function () {
    $.getJSON('/mach/tkawg/play', {
        tkawglabel: tkawglabel
    }, function (data) { })
    .done(function(data) {
        $('button.tkawg.label#' + tkawglabel + ' i.tkawg.fas.fa-wave-square').remove();
        $('button.tkawg.label#' + tkawglabel).append("<i class='tkawg fas fa-wave-square fa-spin fa-3x fa-fw' style='font-size:15px;color:black;'></i> ");
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("PLAYING: " + data.status));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// STOP
$('button#tkawg-stop').click( function () {
    $.getJSON('/mach/tkawg/stop', {
        tkawglabel: tkawglabel
    }, function (data) { })
    .done(function(data) {
        $('button.tkawg.label#' + tkawglabel + ' i.tkawg.fas.fa-wave-square').remove();
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("STOPPED: " + data.status));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
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
        $( "i.tkawg.fa-cog" ).remove();
    })
    .done(function(data) {
        $('button.tkawg.channels[name="channel-' + Channel + '"]').trigger('click');
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("ALL-OFF SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
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
        $('button.tkawg.label#' + tkawglabel + ' i.tkawg.fas.fa-wave-square').remove();
        $("button.tkawg.channels i.tkawg.fa-angle-double-left").remove();
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("CLEAR ALL WAVEFORM SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.tkawg#tkawg-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});