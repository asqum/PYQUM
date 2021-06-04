//when page is loading:
$(document).ready(function(){
    $('div.alzdgcontent').hide();
    $('div.alzdgcontent#settings').show();
    $('div#alzdg-playdata-settings').hide();
    $('div#alzdg-signal-postprocessing').hide();
});

function acquire_play(callback) {
    $( "i.alzdg" ).remove(); //clear previous
    $('button.alzdg.label#'+alzdglabel).prepend("<i class='alzdg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach/alzdg/acquiredata', {
        alzdglabel: alzdglabel,
        recordtime: $('input.alzdg.settings[name="recordtime-scale"]').val(), recordtimeunit: $('input.alzdg.settings[name="recordtime-unit"]').val(),
        recordsum: $('input.alzdg.settings[name="recordsum-scale"]').val(), recordbuff: $('input.alzdg.settings[name="recordbuff-scale"]').val(),
    }, function (data) {
        window.recordsum = data.recordsPerBuff*data.buffersPerAcq
        $('input.alzdg.settings[name="recordtime-scale"]').val(data.datalen);
        $('input.alzdg.settings[name="recordsum-scale"]').val(recordsum);
        $('select.alzdg.data.handling').val("select");
        
        $('div#alzdg-playdata-settings').show();
        $('div#alzdg-signal-postprocessing').show();
        $( "i.alzdg" ).remove(); //clear processing animation

        // Limiting Record Selection based on recordsum provided:
        $('input.alzdg.data.handling').on('mouseup keyup input', function () {
            $(this).val(Math.min(recordsum, Math.max(1, $(this).val()))); // within 1 - recordsum
            });
        
        // play after acquired the DATA:
        playsamples($('input.alzdg.settings[name="recordsum-scale"]').val()-1, $('select.alzdg.data.type').val());
        
        if (typeof callback === "function") callback();
    })
    .done(function(data) {
        $('div.alzdg#alzdg-transfer-time').empty().append($('<h4 style="color: blue;"></h4>')
                                    .text(" (" + data.buffersPerAcq + "*" + data.recordsPerBuff + " in " + (data.transferTime_sec*1000).toFixed(0) + "ms)"));
        $('input.alzdg.settings.records').removeClass('getvalue').addClass('setvalue');
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nStopped at acquire_play" + "\nPlease Refresh!"));
        $('input.alzdg.settings.records').removeClass('setvalue').addClass('getvalue');
    });
};
function playsamples(tracenum, type, average=0, signal_processing='original') {
    $( "i.alzdg" ).remove(); //clear previous
    $('button.alzdg.label#'+alzdglabel).prepend("<i class='alzdg fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach/alzdg/playdata', {
        alzdglabel: alzdglabel, 
        tracenum: tracenum,
        average: average, // mean along y-axis (records)
        signal_processing: signal_processing,
        rotation_compensate: $('input.alzdg.data.rotation_compensate').val(),
        ifreqcorrection: $('input.alzdg.data.ifreqcorrection').val()
    }, function (data) {
        window.t = data.t;
        window.I = data.I;
        window.Q = data.Q;
        window.A = data.A;

        if (type=='time') {
            digplotIQA(t, I, Q, A, "time(s)", "IQA(V)");
        } else if (type=='phase') {
            digplotPhase(I, Q, "I(V)", "Q(V)");
        };
        $( "i.alzdg" ).remove(); //clear processing animation
    })
    .done(function(data) {
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: blue;"></h4>')
                                    .text("PLOTTING TRACE #" + (tracenum+1).toFixed(0)));
        $('input.alzdg.settings.records').removeClass('getvalue').addClass('setvalue');
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        $('input.alzdg.settings.records').removeClass('setvalue').addClass('getvalue');
    });
};
function playrecords(recordsum, type) {
    $.each(Array(recordsum), function(i, value) {
        // console.log("trace #" + i);
        playsamples(i, type)
    });
};
function alzdgplay() {
    var type = $('select.alzdg.data.type').val();
    var handling = $('select.alzdg.data.handling').val();
    var selection = $('input.alzdg.data.handling').val();
    var signal_processing = $('select.alzdg.data.signal_processing').val();
    if (handling=="all") {
        playrecords(recordsum, type);
    } else if (handling=="select") {
        playsamples(selection-1, type, 0, signal_processing);
    } else if (handling=="average") {
        playsamples(selection-1, type, 1, signal_processing);
    };
};

// Functions:
function digplotIQA(x1,y1,y2,y3,xtitle,ytitle) {
    // console.log(xtitle);
    
    let trace1 = {x: [], y: [], mode: 'lines', type: 'scattergl', 
        name: 'I',
        line: {color: 'red', width: 2.5},
        yaxis: 'y' };
    let trace2 = {x: [], y: [], mode: 'lines', type: 'scattergl', 
        name: 'Q',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };
    let trace3 = {x: [], y: [], mode: 'lines', type: 'scattergl', 
        name: 'A',
        line: {color: 'black', width: 2.5},
        // marker: {symbol: 'circle', size: 10, color: 'black'},
        yaxis: 'y' };

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
    
    $.each(x1, function(i, val) {trace1.x.push(val);});
    $.each(y1, function(i, val) {trace1.y.push(val);});
    $.each(x1, function(i, val) {trace2.x.push(val);});
    $.each(y2, function(i, val) {trace2.y.push(val);});
    $.each(x1, function(i, val) {trace3.x.push(val);});
    $.each(y3, function(i, val) {trace3.y.push(val);});

    // console.log("Finished assembled Trace(s)");
    var Trace = [trace1, trace2, trace3];
    Plotly.react('alzdg-IQAP-chart', Trace, layout);
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

function digplotPhase(x1,y1,xtitle,ytitle) {
    var maxscal = Math.max(Math.max(...x1.map(Math.abs)), Math.max(...y1.map(Math.abs)));
    maxscal = maxscal * 1.2;
    // console.log("Limit: " + maxscal);
    
    let traceIQ = {x: [], y: [], mode: 'markers', type: 'scattergl',
        name: 'IQ',
        // line: {color: 'blue', width: 2.5},
        marker: {symbol: 'circle', size: 10, color: 'black'},
        yaxis: 'y' };

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.6,
        width: $(window).width()*0.6,
        xaxis: {
            range: [-maxscal, maxscal],
            zeroline: true,
            title: xtitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            zerolinewidth: 3.5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'red',
        },
        yaxis: {
            range: [-maxscal, maxscal],
            zeroline: true,
            title: ytitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            zerolinewidth: 3.5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'blue',
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
    
    $.each(x1, function(i, val) {traceIQ.x.push(val);});
    $.each(y1, function(i, val) {traceIQ.y.push(val);});

    var Trace = [traceIQ];
    Plotly.react('alzdg-IQAP-chart', Trace, layout);
    // console.log("Finished plotting Trace(s)");
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

//Select model to connect and proceed:
$(function () {
    $('button.alzdg.label').click( function() { /* collecting # of click inside this query-loop! */
        // Make global variable:
        window.alzdglabel = $(this).attr('id');
        console.log(alzdglabel)
        // Indicate current instrument we are operating on:
        $("i.alzdg.fa-check").remove();
        $(this).prepend("<i class='alzdg fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/alzdg/connect', {
            alzdglabel: alzdglabel
        }, function (data) {
            console.log(data.message);
            $('div.alzdg#alzdg-activity').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.alzdg."+alzdglabel+".fa-refresh" ).remove(); //clear previous icon
            // check status
            if (data.status=='connected'){
                $('button.alzdg.label#'+alzdglabel).removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.alzdgcontent').hide();
                $('div.alzdgcontent#settings').show();
                $.getJSON('/mach/alzdg/get', {
                    alzdglabel: alzdglabel
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('input.alzdg.settings').addClass('getvalue');
                    // Model:
                    $('div.alzdg#alzdg-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model'] + " (1-GSPS per Channel)"));
                });
            } else if (data.status=='waiting') {
                $('button.alzdg.label#'+alzdglabel).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.alzdg.label#'+alzdglabel).removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            } else if (data.status=='forbidden') {
                $('button.alzdg.label#'+alzdglabel).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            };
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
 
// Configure Board
$('button.alzdg#configureboard').bind('click', function () {
    $.getJSON('/mach/alzdg/configureboard', {
        alzdglabel: alzdglabel,
        trigdelay: $('input.alzdg.settings[name="trigdelay-scale"]').val(), trigdelayunit: $('input.alzdg.settings[name="trigdelay-unit"]').val()
    }, function (data) {
        console.log(data.message);
        $('input.alzdg.settings[name="trigdelay-scale"]').removeClass('getvalue').addClass('setvalue');
        $('input.alzdg.settings[name="trigdelay-unit"]').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: blue;"></h4>').text("CONFIGURE BOARD SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

// Close Board
$('button.alzdg.closet').bind('click', function () {
    $.getJSON('/mach/alzdg/closet', {
        alzdglabel: alzdglabel
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $('button.alzdg.label#'+alzdglabel).removeClass('error').removeClass('wait').removeClass('connect').addClass('close')
                .prepend("<i class='alzdg "+alzdglabel+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.alzdg').addClass('error');}         
    })
    .done(function(data) {
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.alzdg#alzdg-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

//show log's page
$('button.alzdg.log').bind('click', function () {
    $.getJSON('/mach/alzdg/log', {
        alzdglabel: alzdglabel
    }, function (data) {
        $('div.alzdgcontent').hide();
        $('div.alzdgcontent.log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.alzdgcontent.log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.alzdgcontent.log').show();
        $('button.alzdg').removeClass('selected');
        $('button.alzdg.log').addClass('selected');
    });
    return false;
});

// Loading data first
$('button.alzdg#acquiredata').bind('click', function (e, callback) {
    acquire_play(callback);
    return false;
});
// Play loaded data based on different settings:
$('select.alzdg.data').on('change', function () {
    alzdgplay();
    return false;
});
$('input.alzdg.data.handling').on('change', function () {
    if ($('select.alzdg.data.handling').val()=="select") {
        alzdgplay();
    };
    return false;
})
$('input.alzdg.data.signal').on('change', function () {
    if ($('select.alzdg.data.handling').val()!="all") {
        alzdgplay();
    };
    return false;
})

// live update
$(function () {
    $('input.alzdg.settings.live[name="stream"]').click(function (e, callback) { 
        var stream = $('input.alzdg.settings.live[name="stream"]').is(':checked'); //use css to respond to click / touch
        if (stream == true) {
            $( "i.alzdgplay" ).remove(); //clear previous
            $('button.alzdg#play').prepend("<i class='alzdgplay fas fa-circle-notch fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            $('input.alzdg.settings[name="recordsum-scale"]').val(1); // single-record per stream for real-time inspection
            // LIVE activity:
            acquire_play(callback);
            var alzdgstream = setInterval(acquire_play, 173);
            $('input.alzdg.settings.live[name="stream"]').click(function () {
                clearInterval(alzdgstream); 
                $( "i.alzdgplay" ).remove(); //clear previous
            });
        };
    });
});

// PENDING: saving exported mat-data to client's PC:
$('button.mani#singleqb-savemat').on('click', function() {
    console.log("SAVING MAT FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/export/2dmat', {
        // merely for security screening purposes
        interaction: $('select.mani.singleqb#RO-LO-Frequency').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        console.log('User ' + data.user_name + ' is downloading 2D-Data');
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5300/mach/uploads/2Dsingleqb[' + data.user_name + '].mat',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '2Dsingleqb.mat';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                $('button.mani#singleqb-savemat').hide();
            }
        });
    });
    return false;
});