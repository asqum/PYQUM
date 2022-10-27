//when page is loading:
$(document).ready(function(){
    $('div.adccontent').hide();
    $('div.adccontent#settings').show();
    $('button.adc#acquiredata').hide();
    $('.SDDIG').hide();
    $('div#adc-playdata-settings').hide();
    $('div#adc-signal-postprocessing').hide();
    window.adc_streamlive = false;
});

function acquire_play(callback) {
    $( "i.adc" ).remove(); //clear previous
    $('button.adc.adcname#'+adcname).prepend("<i class='adc fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach/adc/acquiredata', {
        adcname: adcname, adctype: adctype,
        recordtime: $('input.adc.settings[name="recordtime-scale"]').val(), recordtimeunit: $('input.adc.settings[name="recordtime-unit"]').val(),
        recordsum: $('input.adc.settings[name="recordsum-scale"]').val(), recordbuff: $('input.adc.settings[name="recordbuff-scale"]').val(),
        fullscale: $('select.adc.settings.configure.full-scale').val(), iqpair: $('input.adc.settings.SDDIG.IQ-pair').val(),
        FPGA: $('input.adc.settings.FPGA[name="FPGA"]').is(':checked')?1:0,
    }, function (data) {
        window.recordsum = data.recordsPerBuff*data.buffersPerAcq
        $('input.adc.settings[name="recordtime-scale"]').val(data.recordtime_ns);
        $('input.adc.settings[name="recordsum-scale"]').val(recordsum);
        $('select.adc.data.handling').val("select");
        
        $('div#adc-playdata-settings').show();
        $('div#adc-signal-postprocessing').show();
        $( "i.adc" ).remove(); //clear processing animation

        // Limiting Record Selection based on recordsum provided:
        $('input.adc.data.handling').on('mouseup keyup input', function () {
            $(this).val(Math.min(recordsum, Math.max(1, $(this).val()))); // within 1 - recordsum
            });
        
        // play after acquired the DATA:
        playsamples($('input.adc.settings[name="recordsum-scale"]').val()-1, $('select.adc.data.type').val());
        
        if (typeof callback === "function") callback();
    })
    .done(function(data) {
        $('label.parameter.recordbuff').text('= ' + data.buffersPerAcq + ' X');
        $('div.adc#adc-transfer-time').empty().append($('<h4 style="color: blue;"></h4>')
                                    .text(" (" + data.buffersPerAcq + " buff *" + data.recordsPerBuff + " cycles in " + data.transferTime_sec + "s)"));
        $('input.adc.settings.acquire').removeClass('getvalue').addClass('setvalue');
        if (adc_streamlive==true) {
            $( "i.adcplay" ).remove(); //clear previous
            $('button.adc#play').prepend("<i class='adcplay fas fa-circle-notch fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.adc#adc-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nStopped at acquire_play" + "\nPlease Refresh!"));
        $('input.adc.settings.acquire').removeClass('setvalue').addClass('getvalue');
    });
};
function playsamples(tracenum, type, average=0, signal_processing='original') {
    $( "i.adc" ).remove(); //clear previous
    $('button.adc.adcname#'+adcname).prepend("<i class='adc fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach/adc/playdata', {
        adcname: adcname, 
        tracenum: tracenum,
        average: average, // mean along y-axis (records)
        signal_processing: signal_processing,
        rotation_compensate: $('input.adc.data.rotation_compensate').val(),
        ifreqcorrection: $('input.adc.data.ifreqcorrection').val()
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
        $( "i.adc" ).remove(); //clear processing animation
    })
    .done(function(data) {
        $('div.adc#adc-status').empty().append($('<h4 style="color: blue;"></h4>')
                                    .text("PLOTTING TRACE #" + (tracenum+1).toFixed(0)));
        $('input.adc.settings.acquire').removeClass('getvalue').addClass('setvalue');
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.adc#adc-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        $('input.adc.settings.acquire').removeClass('setvalue').addClass('getvalue');
    });
};
function playrecords(recordsum, type) {
    $.each(Array(recordsum), function(i, value) {
        // console.log("trace #" + i);
        playsamples(i, type)
    });
};
function adcplay() {
    var type = $('select.adc.data.type').val();
    var handling = $('select.adc.data.handling').val();
    var selection = $('input.adc.data.handling').val();
    var signal_processing = $('select.adc.data.signal_processing').val();
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
    Plotly.react('adc-IQAP-chart', Trace, layout);
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
    Plotly.react('adc-IQAP-chart', Trace, layout);
    // console.log("Finished plotting Trace(s)");
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

//Select model to connect and proceed:
$(function () {
    $('button.adc.adcname').click( function() {
        // Make global variable:
        window.adcname = $(this).attr('id');
        window.adctype = adcname.split('-')[0];
        $('.'+adctype).show();
        // Indicate current instrument we are operating on:
        $("i.adc.fa-check").remove();
        $(this).prepend("<i class='adc fa fa-check' style='font-size:15px;color:green;'></i> ");
        // connecting to each models:
        $.getJSON('/mach/adc/connect', {
            adcname: adcname, adctype: adctype
        }, function (data) {
            console.log(data.message);
            $('div.adc#adc-activity').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
            $( "i.adc."+adcname+".fa-refresh" ).remove(); //clear previous icon
            // check status
            if (data.status=='connected'){
                $('button.adc.adcname#'+adcname).removeClass('error').removeClass('close').removeClass('wait').addClass('connect');
                // Get ALL value:
                $('div.adccontent').hide();
                $('div.adccontent#settings').show();
                $.getJSON('/mach/adc/get', {
                    adcname: adcname, adctype: adctype
                }, function(data){
                    console.log('Getting:\n' + JSON.stringify(data.message));
                    $('.adc.settings').addClass('getvalue');
                    // Model:
                    $('div.adc#adc-model').empty().append($('<h4 style="color: blue;"></h4>').text(data.message['model'] + " (" + data.message['sampling_rate'] + ")"));
                    $('input.adc.settings[name="recordtime-scale"]').val(data.adc_history['recordtime']);
                    $('input.adc.settings[name="recordsum-scale"]').val(data.adc_history['recordsum']);
                    $('select.adc.settings.configure.full-scale').val(data.adc_history['FULL_SCALE']);
                    $('input.adc.settings.SDDIG.IQ-pair').val(data.adc_history['IQ_PAIR']);
                    $('input.adc.settings[name="trigdelay-scale"]').val(data.adc_history['trigdelay']);
                    $('select.adc.settings.configure.PXI-trigger').val(data.adc_history['PXI']);
                });
            } else if (data.status=='waiting') {
                $('button.adc.adcname#'+adcname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            } else if (data.status=='error') {
                $('button.adc.adcname#'+adcname).removeClass('wait').removeClass('close').removeClass('connect').addClass('error');
            } else if (data.status=='forbidden') {
                $('button.adc.adcname#'+adcname).removeClass('error').removeClass('close').removeClass('connect').addClass('wait');
            };
        })
        .done(function(data) {
            $('div.adc#adc-status').empty().append($('<h4 style="color: blue;"></h4>').text("ACCESSING " + adcname));
        })
        .fail(function(jqxhr, textStatus, error){
            $('div.adc#adc-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        });
        return false;
    });
}); 
 
// Configure Board
$('button.adc#configureboard').bind('click', function () {
    $.getJSON('/mach/adc/configureboard', {
        adcname: adcname, adctype: adctype,
        trigdelay: $('input.adc.settings[name="trigdelay-scale"]').val(), trigdelayunit: $('input.adc.settings[name="trigdelay-unit"]').val(),
        recordtime: $('input.adc.settings[name="recordtime-scale"]').val(), recordtimeunit: $('input.adc.settings[name="recordtime-unit"]').val(),
        recordsum: $('input.adc.settings[name="recordsum-scale"]').val(), recordbuff: $('input.adc.settings[name="recordbuff-scale"]').val(),
        PXI: $('select.adc.settings.configure.PXI-trigger').val(), fullscale: $('select.adc.settings.configure.full-scale').val(),
        FPGA: $('input.adc.settings.FPGA[name="FPGA"]').is(':checked')?1:0,
    }, function (data) {
        $('.adc.settings.configure').removeClass('getvalue').addClass('setvalue');
    })
    .done(function(data) {
        $('div.adc#adc-status').empty().append($('<h4 style="color: blue;"></h4>').text(data.message));
        $('button.adc#acquiredata').show();
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.adc#adc-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
        $('button.adc#acquiredata').hide();
    });
    return false;
});

// Close Board
$('button.adc.closet').bind('click', function () {
    $.getJSON('/mach/adc/closet', {
        adcname: adcname, adctype: adctype
    }, function (data) {
        console.log(data.message);
        if (data.message == "Success"){
            $('button.adc.adcname#'+adcname).removeClass('error').removeClass('wait').removeClass('connect').addClass('close')
                .prepend("<i class='adc "+adcname+" fa fa-refresh' style='font-size:15px;color:green;'></i> ");
        } else {$('button.adc').addClass('error');}         
    })
    .done(function(data) {
        $('div.adc#adc-status').empty().append($('<h4 style="color: blue;"></h4>').text("CLOSED SUCCESSFULLY"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.adc#adc-status').empty().append($('<h4 style="color: red;"></h4>').text(error + "\nPlease Refresh!"));
    });
    return false;
});

//show log's page
$('button.adc.log').bind('click', function () {
    $.getJSON('/mach/adc/log', {
        adcname: adcname, adctype: adctype
    }, function (data) {
        $('div.adccontent').hide();
        $('div.adccontent.log').empty();
        console.log('Based on INSTRLOG, state: ' + data.log['state']);
        $.each(data.log, function(key, value) {
            $('div.adccontent.log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":").
            append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
        });
        $('div.adccontent.log').show();
        $('button.adc').removeClass('selected');
        $('button.adc.log').addClass('selected');
    });
    return false;
});

// Acquire Board: Loading data first
$('button.adc#acquiredata').bind('click', function (e, callback) {
    acquire_play(callback);
    return false;
});
// Play loaded data based on different settings:
$('select.adc.data').on('change', function () {
    adcplay();
    return false;
});
$('input.adc.data.handling').on('change', function () {
    if ($('select.adc.data.handling').val()=="select") {
        adcplay();
    };
    return false;
})
$('input.adc.data.signal').on('change', function () {
    if ($('select.adc.data.handling').val()!="all") {
        adcplay();
    };
    return false;
})

// ReConfigure Board if Record-time (Total-points) and Record-sum (Number of Cycles) had changed:
$('input.adc.settings.records').on('change', function () {
    if (adctype=='SDDIG') { $('button.adc#acquiredata').hide(); };
});
// ReConfigure Board if toggle FPGA:
$('input.adc.settings.FPGA[name="FPGA"]').on('change', function () {
    if (adctype=='SDDIG') { $('button.adc#acquiredata').hide(); };
});

// LIVE update
$(function () {
    $('input.adc.settings.live[name="stream"]').click(function (e, callback) { 
        adc_streamlive = $('input.adc.settings.live[name="stream"]').is(':checked'); //use css to respond to click / touch
        if (adc_streamlive == true) {
            $('input.adc.settings[name="recordsum-scale"]').val(1); // single-record per stream for real-time inspection
            // LIVE activity:
            acquire_play(callback);
            var adcstream = setInterval(acquire_play, 173);
            $('input.adc.settings.live[name="stream"]').click(function () {
                clearInterval(adcstream); 
                $( "i.adcplay" ).remove(); //clear previous
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