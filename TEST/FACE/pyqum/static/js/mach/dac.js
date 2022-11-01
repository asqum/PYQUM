//when page is loading:
$(document).ready(function(){
    $('div.daccontent').hide();
    $('div.daccontent.settings').show();
    $('input.dac.clearQ.waveform').prop( "checked", true ); //default clearQ=1 so that short waveform can be played individually for testing purposes on the Machine page.
    // Globals:
    window.music =[[0],[0],[0],[0]]; 
    window.musicname = [];
    window.musicolor = [];
    window.dacupdate = false;
});

// Functions:
function awgmultiplot(xdata,YDATA,Yname,Ycolor,xtitle,ytitle) {
    // Plotting speed seems nominal.
    // ydata_limit = 3000;
    // xdata = xdata.slice(0, ydata_limit);
    // YDATA = YDATA.slice(0, YDATA.length).map(i => i.slice(0, ydata_limit));
    console.log("xtitle: " + xtitle);
    
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
            zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3,
            gridcolor: 'rgb(159, 197, 232)', zerolinecolor: 'rgb(74, 134, 232)',
        },
        yaxis: {
            zeroline: false, title: ytitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 5,
            gridcolor: 'rgb(159, 197, 232)', zerolinecolor: 'rgb(74, 134, 232)',
        },
        title: 'Arbitrary Waveform Shape (Rough Curve -20X)',
        annotations: [{
            xref: 'paper', yref: 'paper',
            x: 0.03, xanchor: 'right',
            y: 1.05, yanchor: 'bottom',
            text: '', font: {size: 18},
            showarrow: false, textangle: 0
          }]
        };

    Plotly.react('dac-IQAP-chart', Trace, layout);
};
function dac_set_channel(callback) {
    $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text("SETTING CHANNEL " + Channel));
    var ccolor = ['blue','red','cyan','magenta'];
    $.getJSON('/mach/dac/set/channels', {
        dacname: dacname, dactype: dactype, Channel: Channel,
        maxlvl: $('input.dac.scale.source-amplitude').val(),
        maxlvlunit: $('input.dac.unit.source-amplitude').val(),
        // PENDING: offset control
        score: $('textarea.dac.score.setchannels').val(),
        resend: $('input.dac.replace.waveform').is(':checked')?1:0,
        master: $('input.dac.master.trigger').is(':checked')?1:0,
        trigbyPXI: $('select.dac.settings.trigbyPXI').val(),
        markerdelay: $('input.dac.scale.settings.markerdelay').val(),
        markeroption: $('select.dac.setchannels.marker-option').val(),
        clearQ: $('input.dac.clearQ.waveform').is(':checked')?1:0,
    }, function (data) {
        console.log("Waveform CH-" + Channel + " injected.");
        musicname[parseInt(Channel)-1] = "CH-" + Channel;
        musicolor[parseInt(Channel)-1] = ccolor[parseInt(Channel)-1]
        music[parseInt(Channel)-1] = data.music;
        awgmultiplot(data.timeline, music, musicname, musicolor, 'time', 'waveform');
    
        if (typeof callback === "function") callback();
    })
    .done(function(data) {
        $('button.dac.channels[name="channel-' + Channel + '"]').trigger('click');
        $('button.dac.channels[name="channel-' + Channel + '"]' + " i.dac.fa-angle-double-left").remove();
        $('button.dac.channels[name="channel-' + Channel + '"]').append("<i class='dac fas fa-angle-double-left' style='font-size:15px;color:black;'></i> ");
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SET CHANNEL " + Channel + " SUCCESSFULLY"));
        if (dacupdate==true) { 
            $('button.dac.channels[name="channel-' + Channel + '"]' + " i.dac.fas.fa-spinner.fa-pulse").remove(); // clear pulse animation
            $('button.dac.channels[name="channel-' + Channel + '"]').prepend("<i class='dac fas fa-spinner fa-pulse' style='font-size:15px;color:red;'></i> "); };
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
};

//Select model to proceed:
$(function () {
    $('button.dac.dacname').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.dacname = $(this).attr('name');
        window.dactype = dacname.split('-')[0];
        console.log(dacname)
        // Indicate current instrument we are operating on:
        $("i.dac.fa-check").remove();
        $(this).prepend("<i class='dac fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/dac/connect', {
            dacname: dacname, dactype: dactype,
        }, function (data) {
            console.log(data.message);
            $('div.dac#dac-activity').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.dac."+dacname+".fa-refresh" ).remove(); //clear previous icon
            // check status
            if (data.status=='connected'){
                $('button.dac.dacname[name=' + dacname + ']').removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.daccontent').hide();
                $('div.daccontent.settings').show();
                $.getJSON('/mach/dac/get', {
                    dacname: dacname, dactype: dactype,
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.dac.settings').addClass('getvalue');
                    $('input.dac.scale.settings.clockfreq').val(data.message['clockfreq'].split(' ')[0]);
                    $('input.dac.unit.settings.clockfreq').val(data.message['clockfreq'].split(' ')[1]);
                    $('select.dac.settings.trigbyPXI').val(data.message['trigbyPXI']);
                    $('input.dac.scale.settings.markerdelay').val(data.message['markerdelay'])

                    // Checking Play/Run State:
                    $('button.dac.dacname[name=' + dacname + ']' + ' i.dac.fas.fa-wave-square').remove();
                    if(data.message['runstate']==2) {
                        $('button.dac.dacname[name=' + dacname + ']').append("<i class='dac fas fa-wave-square fa-spin fa-3x fa-fw' style='font-size:15px;color:black;'></i> ");
                    };

                    // Checking Waveform-Data inside AWG:
                    $.each(data.message['wlist'], function(i,val) {
                        console.log(i + ". wave-" + val);
                        $('button.dac.channels[name="channel-' + val + '"]' + " i.dac.fa-angle-double-left").remove();
                        $('button.dac.channels[name="channel-' + val + '"]').append("<i class='dac fas fa-angle-double-left' style='font-size:15px;color:black;'></i> ");
                    });

                    // Checking Readiness (Waveform presence): SDAWG ONLY
                    if (dactype=="SDAWG") {
                        console.log("readiness: " + data.message['ready2play']);
                        $.each(data.message['ready2play'], function(i,val) {
                            $('button.dac.channels[name="channel-' + (i+1) + '"]' + " i.dac.fa-angle-double-left").remove();
                            if (val>0) {
                                $('button.dac.channels[name="channel-' + (i+1) + '"]').append("<i class='dac fas fa-angle-double-left' style='font-size:15px;color:black;'></i> ");
                            };
                        });
                    };

                    // Query only output:
                    $('div.dac#dac-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model']));
                });
            } else if (data.status=='waiting') {
                $('button.dac.dacname[name=' + dacname + ']').removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.dac.dacname[name=' + dacname + ']').removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            } else if (data.status=='forbidden') {
                $('button.dac.dacname[name=' + dacname + ']').removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            };
        })
        .done(function(data) {
            $('div.dac#dac-status').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + dacname));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.dac#dac-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 

// Setting Clock Frequency
$('input.dac.clockfreq').change( function () { // the enter key code
    $.getJSON('/mach/dac/set/clockfreq', {
        dacname: dacname, dactype: dactype,
        clockfreq: $('input.dac.scale.clockfreq').val(), clockfrequnit: $('input.dac.unit.clockfreq').val()
    }, function (data) { 
        console.log(Date($.now()) + ':\nSetting ' + data.message);
        $('input.dac.settings.clockfreq').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.dac#dac-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOCK-FREQUENCY ADJUSTED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// close & reset = closet OR re-connect
$('button.dac.closet').bind('click', function () {
    $.getJSON('/mach/dac/closet', {
        dacname: dacname, dactype: dactype,
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            // $('select.dac[name="dacname"]').find('option[value='+dacname+']').removeClass('connect').addClass('close')
                // .prepend("<i class='dso fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
            $( "i.dac."+dacname+".fa-wifi" ).remove();
            $('button.dac.dacname[name=' + dacname + ']').removeClass('error').removeClass('wait').removeClass('connect').addClass('close')
                .prepend("<i class='dac "+dacname+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.dac').addClass('error');}         
    })
    .done(function(data) {
        $('div.dac#dac-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// Test the flow / script for use in measurement
$('button.dac#dac-testing').bind('click', function () {
    $( "i.dac.fa-cog" ).remove(); //clear previous
    $('button.dac.dacname[name=' + dacname + ']').prepend("<i class='dac fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/dac/testing', {
        dacname: dacname, dactype: dactype,
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $( "i.dac.fa-cog" ).remove();
        } else {$('button.dac').addClass('error');}         
    })
    .done(function(data) {
        $('div.dac#dac-status').empty().append($('<h4 style="color: blue;"></h4>').text("TEST-FLOW SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

//show log's page
$('button.dac.log').bind('click', function () {
    // Indicate current spec we are inspecting on current instrument:
    $("i.dac.fa-angle-double-right").remove();
    $(this).prepend("<i class='dac fas fa-angle-double-right' style='font-size:15px;color:black;'></i> ");
    $.getJSON('/mach/dac/log', {
        dacname: dacname, dactype: dactype,
    }, function (data) {
        $('div.daccontent').hide();
        $('div.daccontent.log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.daccontent.log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.daccontent.log').show();
        $('button.dac').removeClass('selected');
        $('button.dac.log').addClass('selected');
    });
    return false;
});

// Getting Channel:
$('button.dac.channels').bind('click', function () {
    // Which Channel:
    window.Channel = $(this).attr('name').split('-')[1];
    console.log("Setting " + dactype + "'s Channel-" + Channel);
    // Indicate current spec we are inspecting on current instrument:
    $("i.dac.fa-angle-double-right").remove();
    $(this).prepend("<i class='dac fas fa-angle-double-right' style='font-size:15px;color:black;'></i> ");
    $.getJSON('/mach/dac/get/channels', {
        dacname: dacname, dactype: dactype, Channel: Channel
    }, function (data) {
        $('div.daccontent').hide();
        $('div.daccontent.setchannels').show();
        console.log(data.message);
        $('textarea.dac.score.setchannels').val(data.message['score']);
        $('input.dac.scale.source-amplitude').val(data.message['source-amplitude'].split(' ')[0]);
        $('input.dac.unit.source-amplitude').val(data.message['source-amplitude'].split(' ')[1]);
        $('input.dac.scale.source-offset').val(data.message['source-offset'].split(' ')[0]);
        $('input.dac.unit.source-offset').val(data.message['source-offset'].split(' ')[1]);
        $('input.dac.setchannels.output').prop( "checked", Boolean(data.message['chstate']) );
        $('input.dac.replace.waveform').prop( "checked", Boolean(data.message['resend']) );
        $('input.dac.master.trigger').prop( "checked", Boolean(data.message['master']) );
        $('select.dac.setchannels.marker-option').val(data.message['markeroption']);
        $('button.dac').removeClass('selected');
        $('button.dac.channels[name="channel-' + Channel + '"]').addClass('selected');
    })
    .done(function(data) {
        if (Boolean(data.message['resend'])==true) {
            $('button.dac.dacname[name=' + dacname + ']' + ' i.dac.fas.fa-wave-square').remove();
            $('button.dac.dacname[name=' + dacname + ']').append("<i class='dac fas fa-wave-square fa-spin fa-3x fa-fw' style='font-size:15px;color:black;'></i> ");
        };
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\n" + status + "\nPlease Refresh!"));
    });
    return false;
});

// Initiate Score with Pulse-period:
$("input.dac.initscore").bind('click', function () {
    var pperiod = $('input.dac.scale.setchannels.pulse-period').val();
    var pperiodunit = $('input.dac.unit.setchannels.pulse-period').val();
    $('textarea.dac.score.setchannels').val(pperiodunit + "=" + pperiod + ";\n");
    $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SCORE INITIATED WITH LENGTH " + pperiod + pperiodunit));
    return false;
});
// Inserting shapes into score sheet:
$('input.dac.shapes.setchannels').bind('click', function () {
    var lascore = $('textarea.dac.score.setchannels').val();
    $('textarea.dac.score.setchannels').val(lascore + $(this).val() + '/,' + $('input.dac.scale.setchannels.pulse-width').val() + ',' 
                                                                        + $('input.dac.scale.setchannels.pulse-height').val() + ';\n');
    console.log('adding: ' + $(this).val());
    return false;
});

// Score (Injecting waveform-data into DAC):
$('button#dac-score').click( function () {
    dac_set_channel();
    return false;
});
// Set Channel State:
$('input.dac.setchannels.output').change(function () {
    var state = $('input.dac.setchannels.output').is(':checked')?1:0;
    $.getJSON('/mach/dac/output/channels', {
        dacname: dacname, dactype: dactype, Channel: Channel, state: state,
    }, function (data) {
        var status = data.status;
    })
    .done(function(data) {
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("SET CHANNEL " + Channel + ": " + Boolean(state)));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\n" + status + "\nPlease Refresh!"));
    });
    return false;
});
// PLAY
$('button#dac-play').click( function () {
    $.getJSON('/mach/dac/play', {
        dacname: dacname, dactype: dactype,
    }, function (data) { })
    .done(function(data) {
        $('button.dac.channels[name="channel-' + Channel + '"]').trigger('click');
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("START PLAYING: " + data.status));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// LIVE DAC UPDATE:
$(function () {
    $('input.dac.live-update-channel').click(function (e, callback) { 
        dacupdate = $('input.dac.live-update-channel').is(':checked'); //use css to respond to click / touch
        if (dacupdate == true) {
            
            // LIVE activity:
            dac_set_channel(callback);
            var dacstream = setInterval(dac_set_channel, 1730);
            $('input.dac.live-update-channel').click(function () {
                clearInterval(dacstream); 
                
                $('button.dac.channels[name="channel-' + Channel + '"]' + " i.dac.fas.fa-spinner.fa-pulse").remove(); // clear pulse animation
            });
        };
    });
});
$('input.dac.live-update-channel').click(function () {
    dacupdate = $('input.dac.live-update-channel').is(':checked')?1:0;
    $.getJSON('/mach/dac/live/update/channel', { dacname:dacname, Channel:Channel, dacupdate:dacupdate }, function(data) { console.log(data.message); });
    // return false;
});

// STOP
$('button#dac-stop').click( function () {
    $.getJSON('/mach/dac/stop', {
        dacname: dacname, dactype: dactype,
    }, function (data) { })
    .done(function(data) {
        $('button.dac.dacname[name=' + dacname + ']' + ' i.dac.fas.fa-wave-square').remove();
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("STOPPED: " + data.status));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// All Off
$('button.dac#dac-alloff').bind('click', function () {
    $( "i.dac.fa-cog" ).remove(); //clear previous
    $('button.dac.dacname[name=' + dacname + ']').prepend("<i class='dac fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/dac/alloff', {
        dacname: dacname, dactype: dactype,
    }, function (data) {
        console.log("All-Off: " + data.message);
        $( "i.dac.fa-cog" ).remove();
    })
    .done(function(data) {
        $('button.dac.channels[name="channel-' + Channel + '"]').trigger('click');
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("ALL-OFF SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});
// Clear ALL (Waveform)
$('button.dac#dac-clearall').bind('click', function () {
    $( "i.dac.fa-cog" ).remove(); //clear previous
    $('button.dac.dacname[name=' + dacname + ']').prepend("<i class='dac fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $.getJSON('/mach/dac/clearall', {
        dacname: dacname, dactype: dactype,
    }, function (data) {
        console.log("Clear-All: " + data.message);
        $( "i.dac.fa-cog" ).remove();         
    })
    .done(function(data) {
        $('button.dac.channels[name="channel-' + Channel + '"]').trigger('click');
        $('button.dac.dacname[name=' + dacname + ']' + ' i.dac.fas.fa-wave-square').remove();
        $("button.dac.channels i.dac.fa-angle-double-left").remove();
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: blue;"></h4>').text("CLEAR ALL WAVEFORM SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.dac#dac-chstatus').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});