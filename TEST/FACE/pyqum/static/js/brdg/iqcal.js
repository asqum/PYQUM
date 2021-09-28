$(document).ready(function(){
    // $('div.iqcalcontent').show();
    $('div.sweeping-spectrum').prepend("<i class='fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $('div.sweeping-spectrum').hide();
    $('.iqcal.auto.AI.run').hide();
    $('.iqcal.auto.AI.stop').hide();
});

// When page loads:
$( function() {
    // load module-list:
    var mixermodule_list = [];
    $.getJSON("/bridge/iqcal/load/mixermodules", {}, function (data) {
        $.each(data.mixermodule_list, function(i,mixermodule) {
            mixermodule_list.push(mixermodule);
        });
        console.log(mixermodule_list.join(', '));
        $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: red;"></h4>').text("Total IQ-corrections available: " + mixermodule_list.length));
    });
    
    // Auto-complete:
    // mixermodule_list is still empty outside here: weird.
    $( "input.iqcal.mixer-module-KEY" ).autocomplete({
        source: mixermodule_list
    });

    // check auto IQCAL:
    check_auto_iqcal();
});

// Functions:
function plot_sidebands(x1,y1,x2,y2,xtitle,ytitle) {
    let trace1 = {x: [], y: [], mode: 'markers', type: 'scattergl',//'bar', 
        name: 'Zero-span',
        // line: {color: 'red', width: 2.5},
        marker: {symbol: 'circle', size: 17, color: 'red'},
        yaxis: 'y' };
    let trace2 = {x: [], y: [], mode: 'lines', type: 'scattergl',//'bar', 
        name: 'Full-sweep', line: {color: 'blue', width: 2.5}, yaxis: 'y' };
    
    let layout = {
        legend: {x: 1.08}, height: $(window).height()*0.66, width: $(window).width()*0.7,
        xaxis: {
            zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3,
            gridcolor: 'rgb(159, 197, 232)', zerolinecolor: 'rgb(74, 134, 232)',
        },
        yaxis: {
            zeroline: false, title: ytitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 5, 
            gridcolor: 'rgb(159, 197, 232)', zerolinecolor: 'rgb(74, 134, 232)',
        },
        title: 'Scouting Power-Spectrum',
        annotations: [{
            xref: 'paper', yref: 'paper', x: 0.03, xanchor: 'right', y: 1.05, yanchor: 'bottom', text: '', font: {size: 18}, showarrow: false, textangle: 0
          }]
        };
    
    $.each(x1, function(i, val) {trace1.x.push(val);});
    $.each(y1, function(i, val) {trace1.y.push(val);});
    $.each(x2, function(i, val) {trace2.x.push(val);});
    $.each(y2, function(i, val) {trace2.y.push(val);});

    var Trace = [trace1,trace2];
    Plotly.react('iqcal-SA-scouting', Trace, layout);
};
function manual_calibrate() {
    $('div.sweeping-spectrum').show();
    var mixermodule_key = $("input.iqcal.mixer-module-KEY").val();
    var mixermodule_val = $("input.iqcal.mixer-module-VAL").val();
    var LO_frequency_GHz = $("input.iqcal.manual.LO-frequency-GHz").val();
    var IF_frequency_MHz = $("input.iqcal.manual.IF-frequency-MHz").val();
    var Sweep_points = $("input.iqcal.manual.Sweep-points").val();
    var RBW_kHz = $("input.iqcal.manual.RBW_kHz").val();
    var AveCount = $("input.iqcal.manual.AveCount").val();
    $.getJSON("/bridge/iqcal/manual/calibrate", {
        mixermodule_key: mixermodule_key, mixermodule_val: mixermodule_val,
        LO_frequency_GHz: LO_frequency_GHz, IF_frequency_MHz: IF_frequency_MHz, Sweep_points: Sweep_points, RBW_kHz: RBW_kHz, AveCount: AveCount,
    }, function () {
        console.log("IQ-Calibration library has been updated.");
    })
    .done( function (data) {
        $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: blue;"></h4>').text(mixermodule_key + " has just been updated. "));
        plot_sidebands(data.freq_list, data.powa_list, data.full_spectrum_x, data.full_spectrum_y, 'Frequency (GHz)','Power (dBm)');
        $('div.sweeping-spectrum').hide();
        $('.iqcal > label#iqcal-message').append($('<h4 style="color: blue;"></h4>')
            .text("Red-band: " + data.powa_list[1].toFixed(3) + ", LO-Leak: " + data.powa_list[2].toFixed(3) + ", Blue-band: " + data.powa_list[3].toFixed(3) + ". "));
    });
};
function check_auto_iqcal() {
    $("input.iqcal.mixer-module-KEY").val($('input.iqcal.auto.AI.Mixer-module').val() + "i" + $('input.iqcal.auto.AI.IF-rotation-MHz').val()).trigger("change");
    $.getJSON("/bridge/iqcal/auto/check/status", {}, function (data) {
        console.log("running: " + data.running + ", iteration: " + data.iteration + ", autoIQCAL_dur_s: " + data.autoIQCAL_dur_s);
        if (data.running==true) { 
            $('.iqcal.auto.AI.run').hide();
            $('.iqcal.auto.AI.stop').show();
        } else {
            $('.iqcal.auto.AI.stop').hide();
            $('.iqcal.auto.AI.run').show();
        };
        $('.iqcal > label#auto-iqcal-update').empty().append($('<h4 style="color: blue;"></h4>')
                .text("Last iteration-" + data.iteration + " took " + data.autoIQCAL_dur_s + "-sec to improve: "));
        plot_sidebands([],[],data.autoIQCAL_frequencies,data.autoIQCAL_spectrum,"Frequency (GHz)","Power (dBm)");
    });
};


// Check Live DAC-CH:
$(document).on("click", "input.iqcal.mixer-module-KEY", function () {
    $.getJSON("/bridge/iqcal/check/daclive", {}, function (data) {
        $('label#iqcal-live-dach').empty().append($('<h4 style="color: green;"></h4>').text("LIVE: " + data.live_dac_channel.join(', ')));
    });
    return false;
});
// Loading Calibration:
$(document).on("change", "input.iqcal.mixer-module-KEY", function () {
    $.getJSON("/bridge/iqcal/load/calibrate", {
        mixermodule_key: $("input.iqcal.mixer-module-KEY").val(),
    }, function (data) {
        $("input.iqcal.mixer-module-VAL").val(data.mixermodule_val);
        if (data.mixermodule_val=="no-module-found") {
            $("input.iqcal.mixer-module-VAL").css("color", "red");
        } else { $("input.iqcal.mixer-module-VAL").css("color", "black"); };
    });
    return false;
});
// Manual Calibration:
$(document).on("change", "input.iqcal.manual.SA.sweep", function () {
    manual_calibrate();
    return false;
});

// SA CONNECTION:
$(function () {
    $('input.iqcal.manual.SA.connect').click(function (e, callback) { 
        saconnect = $('input.iqcal.manual.SA.connect').is(':checked'); //use css to respond to click / touch
        if (saconnect == true) {
            $.getJSON("/bridge/iqcal/manual/sa/connect", {}, function (data) { console.log("status: " + data.status) })
            .done( function (data) { $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: blue;"></h4>').text(data.status)); })
            .fail(function(jqxhr, textStatus, error){ $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: blue;"></h4>').text(error + "\nPlease Refresh!")); });
        } else {
            $.getJSON("/bridge/iqcal/manual/sa/closet", {}, function (data) { console.log("status: " + data.status) })
            .done( function (data) { $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: red;"></h4>').text(data.status)); })
            .fail(function(jqxhr, textStatus, error){ $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: blue;"></h4>').text(error + "\nPlease Refresh!")); });
        };
    });
});

// AUTO IQ-CALIBRATION:
// LIVE UPDATE STATUS:
$(function () {
    $('input.iqcal.auto.status').click(function () { 
        var livestat = $('input.iqcal.auto.status').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            check_auto_iqcal();
            var live_loop = setInterval(check_auto_iqcal, 3170);
            $('input.iqcal.auto.status').click(function () {
                clearInterval(live_loop); 
            });
        };
    });
});
// RUN:
$(function () {
    $("a.iqcal.auto.AI.run").click( function() {
        if ($('input.iqcal.auto.status').is(':checked')==false) { $('input.iqcal.auto.status').trigger("click"); }; // CLICK-ON the LIVE-UPDATE-STATUS
        $.getJSON("/bridge/iqcal/auto/calibrate/run", {
            Conv_frequency_GHz: $('input.iqcal.auto.AI.Conv-frequency-GHz').val(),
            IF_rotation_MHz: $('input.iqcal.auto.AI.IF-rotation-MHz').val(),
            LO_power_dBm: $('input.iqcal.auto.AI.LO-power-dBm').val(),
            IF_period_ns: $('input.iqcal.auto.AI.IF-period-ns').val(),
            IF_scale: $('input.iqcal.auto.AI.IF-scale').val(),
            Mixer_module: $('input.iqcal.auto.AI.Mixer-module').val(),
            Wiring_config: $('input.iqcal.auto.AI.Wiring-config').val(),
            Channels_group: $('input.iqcal.auto.AI.Channels-group').val(),
        }, function (data) {
            $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
        });
        return false;
    });
});
// STOP:
$(function () {
    $("a.iqcal.auto.AI.stop").click( function() {
        if ($('input.iqcal.auto.status').is(':checked')==false) { $('input.iqcal.auto.status').trigger("click"); }; // CLICK-ON the LIVE-UPDATE-STATUS
        $.getJSON("/bridge/iqcal/auto/calibrate/stop", {}, function (data) {
            $('.iqcal > label#iqcal-message').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
        });
        return false;
    });
});

$(function () {
    $("#iqcal-tab").click( function () {
        

        return false;
    });
});